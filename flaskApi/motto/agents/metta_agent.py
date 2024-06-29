# from .db.genecode import Genecode
from .db.ontology import get_ontology_term, fetch_ontology_terms
from .db.pathway import fetch_pathway_data
from .db.genecode import fetch_genecode_data
from .agent import Agent, Response
from hyperon import MeTTa, Environment, ExpressionAtom, OperationAtom, E, S, interpret, ValueAtom
from .gpt_agent import ChatGPTAgent
from .llama_agent import LlamaAgent
import ast


class MettaAgent(Agent):

    def _try_unwrap(self, val):
        if val is None or isinstance(val, str):
            return val
        return repr(val)

    def __init__(self, path=None, code=None, atoms={}, include_paths=None):
        self._path = self._try_unwrap(path)
        self._code = code.get_children()[1] if isinstance(code, ExpressionAtom) else \
                     self._try_unwrap(code)
        if path is None and code is None:
            raise RuntimeError(f"{self.__class__.__name__} requires either path or code")
        self._atoms = atoms
        self._includes = include_paths

    def _prepare(self, metta, msgs_atom):
        for k, v in self._atoms.items():
            metta.register_atom(k, v)
        metta.space().add_atom(E(S('='), E(S('messages')), msgs_atom))

    def _postproc(self, response):
        results = []
        # Multiple responses are now returned as a list
        for rs in response:
            for r in rs:
                if isinstance(r, ExpressionAtom):
                    ch = r.get_children()
                    if len(ch) == 0:
                        continue
                    # FIXME? we can simply ignore all non-Response results
                    if len(ch) != 2 or repr(ch[0]) != 'Response':
                        raise TypeError(f"Unexpected response format {ch}")
                    results += [ch[1]]
        return Response(results, None)

    def __call__(self, msgs_atom, functions=[]):
        # FIXME: we cannot use higher-level metta here (e.g. passed by llm func),
        # from which an agent can be called, because its space will be polluted.
        # Thus, we create new metta runner and import motto.
        # We could avoid importing motto each time by reusing tokenizer or by
        # swapping its space with a temporary space, but current API is not enough.
        # It could also be possible to import! the agent script into a new space,
        # but there is no function to do this without creating a new token
        # (which might be useful). The latter solution will work differently.
        if self._includes is not None:
            env_builder = Environment.custom_env(include_paths=self._includes)
            metta = MeTTa(env_builder=env_builder)
        else:
            metta = MeTTa()
        # TODO: assert
        metta.run("!(import! &self motto)")
        #metta.load_module_at_path("motto")
        # TODO: support {'role': , 'content': } dict input
        if isinstance(msgs_atom, str):
            msgs_atom = metta.parse_single(msgs_atom)
        self._prepare(metta, msgs_atom)
        if self._path is not None:
            #response = metta.load_module_at_path(self._path)
            with open(self._path, mode='r') as f:
                code = f.read()
                response = metta.run(code)
                # print("response: ",response)
                mettaResponse = self._postproc(response)

                print("metta response", mettaResponse)
                ch = mettaResponse.content[0].get_children()
                

                response2 = ""
                mes = ""
                
                if str(ch[0]) == "ontology_term":
                    ontology_terms = [str(term.get_children()[1]) for term in mettaResponse.content if str(term.get_children()[0]) == "ontology_term"]
                    response2 = fetch_ontology_terms(ontology_terms)
                elif str(ch[0]) == "pathway":
                    response2 = fetch_pathway_data(mettaResponse.content)
                elif str(ch[0]) == 'transcript':
                    response2 = fetch_genecode_data(mettaResponse.content)              
                
                agent = LlamaAgent()
                functions = []
                params = {}
                message = f"Below is a user's question and the answer for the user's question. By getting a context from the user's question, make the response more descriptive. You can get an accurate information from the dataset that's provided below when generating more descriptions. \n\
                \n User's question: {msgs_atom} \n\
                \n dataset: {response2} \n\
                \n response for the user's question: {mettaResponse} \n\
                \n Return only the description, don't include sentences like here is the description and also others.\n"


                # messages = [{'role': 'user', 'content': str(message)}]
                naturalLanguageResponse = agent(message, **params)
                naturalLanguageResponse = Response([ValueAtom(naturalLanguageResponse.text)])
        if self._code is not None:
            response = metta.run(self._code) if isinstance(self._code, str) else \
                       [interpret(metta.space(), self._code)]
            return self._postproc(response)
        return naturalLanguageResponse

class DialogAgent(MettaAgent):

    def __init__(self, path=None, code=None, atoms={}, include_paths=None):
        self.history = []
        super().__init__(path, code, atoms, include_paths)

    def _prepare(self, metta, msgs_atom):
        super()._prepare(metta, msgs_atom)
        metta.space().add_atom(E(S('='), E(S('history')),
                                 E(S('Messages'), *self.history)))
        # atm, we put the input message into the history by default
        self.history += [msgs_atom]

    def _postproc(self, response):
        # TODO it's very initial version of post-processing
        # The output is added to the history as the assistant utterance.
        # This might be ok: if someone wants to avoid this, Function
        # (TODO not supported yet) instead of Response could be used.
        # But one can add explicit commands for putting something into
        # the history as well as to do other stuff
        result = super()._postproc(response)
        # TODO: 0 or >1 results, to expression?
        self.history += [E(S('assistant'), result.content[0])]
        return result
