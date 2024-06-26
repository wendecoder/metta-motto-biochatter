import os
from hyperon import *
from hyperon.ext import register_atoms
from .llm_connect import GptConversation
from .prompts import BioCypherPromptEngine
from pathlib import Path

def biochatter_metta(metta: MeTTa, *args):

    for atom in args:
        user_question = str(atom) 
    
    pwd = Path(__file__).parent

    prompt_engine = BioCypherPromptEngine(
                        model_name="gpt-3.5-turbo",
                        schema_config_or_info_path=f"{pwd}/biocypher_config/schema_config.yaml",
                    )
    """ Gene Ontology Atomspace queries: """
    metta_query = prompt_engine.generate_query(user_question)
    metta_query = f"!(match &space \n {metta_query} \n)"
 
    return [ValueAtom(metta_query)]
