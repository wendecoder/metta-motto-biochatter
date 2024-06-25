class MettaPrompt:

    def __init__(self, schema_nodes, schema_edges) -> None:
        self.schema_nodes = schema_nodes
        self.schema_edges = schema_edges

    def generate_metta_node_samples(self) -> str:
        if not self.schema_nodes:
            return ''
        
        metta_node_sample = "\nThe following are the representations of the nodes in the dataset: \n###\n"

        for node_label, properties in self.schema_nodes.items():
            metta_node_sample += f"; This is the format of the nodes for '{node_label}': \n"
            metta_node_sample += f"({node_label} <{node_label}_id>)\n"
            for prop, prop_type in properties.items():
                # Skip propeties that are not usually mapped to the MeTTa files
                if prop in ['source', 'source_url', 'version']:
                    continue
                metta_node_sample += f"({prop} ({node_label} <{node_label}_id>) <value_of_type_{prop_type}>)\n"
    
        metta_node_sample += "### \n"
        return metta_node_sample

    def generate_metta_edge_samples(self):
        if not self.schema_edges:
            return ''
        
        metta_edge_sample = "\nThe following are the representations of the edges in the dataset: \n###\n"

        for edge_label, attributes in self.schema_edges.items():
            source = attributes['source']
            target = attributes['target']
            properties = attributes['properties']

            description = attributes.get('description', None)
            full_name = attributes.get('full_name', None)

            if full_name: metta_edge_sample += f"; The name '{edge_label}' is just a short form of \"{full_name}\". \n"
            if description: metta_edge_sample += f"; The relationship '{edge_label}' would be described as: \"{description}\". \n"
            metta_edge_sample += f"; These is the format of the edges for '{edge_label}': \n"
            metta_edge_sample += f"({edge_label} ({source} <{source}_id>) ({target} <{target}_id>))\n"
            for prop, prop_type in properties.items():
                # Skip propeties that are not usually mapped to the MeTTa files
                if prop in ['source', 'source_url', 'version']:
                    continue
                metta_edge_sample += f"({prop} ({edge_label} ({source} <{source}_id>) ({target} <{target}_id>)) <value_of_type_{prop_type}>)\n"
    
        metta_edge_sample += "### \n"
        return metta_edge_sample

    def generate_metta_node_query_samples(self):
        if not self.schema_nodes:
            return ''
        
        node_query_samples = "\nThe following are sample queries for the nodes in the dataset: \n***\n"

        for node_label, properties in self.schema_nodes.items():
            node_query_samples += f"\n; Get properties of a '{node_label}' with some id <{node_label}_id>: \n\
                                        ($prop ({node_label} <{node_label}_id>) $val)\n\
                                        ($prop $val)\n"

            for prop, _ in properties.items():
                # Skip propeties that are not usually mapped to the MeTTa files
                if prop in ['source', 'source_url', 'version']:
                    continue

                node_query_samples += f"\n; Get the '{prop}' property of some '{node_label}' with id <{node_label}_id>: \n\
                                            ({prop} ({node_label} <{node_label}_id>) $val)\n\
                                            $val\n"

                node_query_samples += f"\n; Get the properties of a '{node_label}' with '{prop}' of <some_{prop}_val>: \n\
                                            (,\n\
                                             ({prop} ({node_label} $id) <some_{prop}_val>)\n\
                                             ($prop ({node_label} $id) $val)\n\
                                            )\n\
                                            ($prop $val)\n"
            if node_label == "gene":
                node_query_samples += f"\n Below are some examples of questions and their corresponding queries on gene. \n***\n\
                \n ;Get properties of gene <some_gene_ensembl_id> \n\
                ($prop (gene <some_gene_ensembl_id>) $val) \n\
                ($prop $val) \n\
                \n ;Get properties of gene <some_gene_HGNC_symbol> (use the gene HGNC symbol instead of ensembl id) \n\
                    (, \n\
                        (gene_name (gene $ens) <some_gene_HGNC_symbol>) \n\
                        ($prop (gene $ens) $val) \n\
                    ) \n\
                    ($prop $val) \n"
        node_query_samples += "*** \n"
        return node_query_samples

    def generate_metta_edge_query_samples(self):
        if not self.schema_edges:
            return ''
        
        edge_query_samples = "\nThe following are sample queries for the edges in the dataset: \n***\n"

        for edge_label, attributes in self.schema_edges.items():
            source = attributes['source']
            target = attributes['target']
            properties = attributes['properties']

            edge_query_samples += f"; Find the '{target} nodes' of the '{source}' with id <{source}_id>:\n\
                                    ({edge_label} ({source} <{source}_id>) ${target}_node)\n\
                                    ${target}_node\n"

            for prop, prop_type in properties.items():
                # Skip propeties that are not usually mapped to the MeTTa files
                if prop in ['source', 'source_url', 'version']:
                    continue

                edge_query_samples += f"; Find the '{target} nodes' of a '{source}' with '{prop}' of <some_{prop}_val>:\n\
                                        (,\n\
                                         ({prop} ({source} $id) <some_{prop}_val>)\n\
                                         ({edge_label} ({source} $id) ${target}_node)\n\
                                        )\n\
                                        ${target}_node\n"

        edge_query_samples += "*** \n"
        return edge_query_samples

    def generate_transcripts_edge_query_samples(self):
        transcripts_edge_query_samples = self.generate_metta_edge_query_samples()
        transcripts_edge_query_samples += f"\n Below are some examples of questions and their corresponding query on transcripts \n***\n\
        \n ;Find the transcripts of gene <some_gene_ensembl_id> \n\
        (transcribed_to (gene <some_gene_ensembl_id>) $transcript) \n\
        ($transcript) \n\
        \n;Find the transcripts of gene <some_gene_HGNC_symbol> (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) <some_gene_HGNC_symbol>) \n\
            (transcribed_to (gene $ens) $transcript) \n\
        )\n\
        $transcript \n"

        transcripts_edge_query_samples += "*** \n"
        return transcripts_edge_query_samples

    def generate_pathway_edge_query_samples(self):
        pathway_edge_query_samples = self.generate_metta_edge_query_samples()
        pathway_edge_query_samples += f"\n Below are some examples of questions and their corresponding query on pathways \n***\n\
        \n ;Find pathways that gene <some_gene_ensembl_id> is a subset of \n\
        (, \n\
            (genes_pathways (gene <some_gene_ensembl_id>) $p) \n\
        ) \n\
        $p \n\
        \n ;Find pathways that gene ENSG00000000938 is a subset of \n\
        (, \n\
            (genes_pathways (gene ENSG00000000938) $p) \n\
        ) \n\
        $p \n\
        \n ;Find pathways that gene ENSG00000177508 is a subset of \n\
        (, \n\
            (genes_pathways (gene ENSG00000177508) $p) \n\
        ) \n\
        $p \n\
        \n ;Find pathways that gene <some_gene_HGNC_symbol> is a subset of (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
                (gene_name (gene $ens) <some_gene_HGNC_symbol>) \n\
                (genes_pathways (gene $ens) $p) \n\
        )\n\
        $p \n\
        \n ;Find pathways that gene PPID is a subset of (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
                (gene_name (gene $ens) PPID) \n\
                (genes_pathways (gene $ens) $p) \n\
        )\n\
        $p \n\
        \n ;Find pathways that gene DDX11L1 is a subset of (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
                (gene_name (gene $ens) DDX11L1) \n\
                (genes_pathways (gene $ens) $p) \n\
        )\n\
        $p \n\
        \n ;Find parent pathways of the pathways that gene <some_gene_ensembl_id> is a subset of.\n\
        (, \n\
            (genes_pathways (gene <some_gene_ensembl_id>) $p1) \n\
            (parent_pathway_of $p2 $p1) \n\
        ) \n\
        $p2 \n\
        \n ;Find parent pathways of the pathways that gene ENSG00000000938  is a subset of.\n\
        (, \n\
            (genes_pathways (gene ENSG00000000938) $p1) \n\
            (parent_pathway_of $p2 $p1) \n\
        ) \n\
        $p2 \n\
        \n ;Find parent pathways of the pathways that gene ENSG00000177508  is a subset of.\n\
        (, \n\
            (genes_pathways (gene ENSG00000177508) $p1) \n\
            (parent_pathway_of $p2 $p1) \n\
        ) \n\
        $p2 \n\
        \n ;Find parent pathways of the pathways that gene  is a subset of (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) <some_gene_HGNC_symbol>) \n\
            (genes_pathways (gene $ens) $p1) \n\
            (parent_pathway_of $p2 $p1) \n\
        ) \n\
        $p2 \n\
        \n ;Find parent pathways of the pathways that gene PPID is a subset of (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) PPID) \n\
            (genes_pathways (gene $ens) $p1) \n\
            (parent_pathway_of $p2 $p1) \n\
        ) \n\
        $p2 \n\
        \n ;Find parent pathways of the pathways that gene DDX11L1 is a subset of (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) DDX11L1) \n\
            (genes_pathways (gene $ens) $p1) \n\
            (parent_pathway_of $p2 $p1) \n\
        ) \n\
        $p2 \n"
        pathway_edge_query_samples += "*** \n"
        return pathway_edge_query_samples

    def generate_gene_ontology_edge_query_samples(self):
        gene_ontology_edge_query_samples = self.generate_metta_edge_query_samples()
        gene_ontology_edge_query_samples += f"\n Below are some examples of questions and their corresponding query on pathways \n***\n\
        \n ;Find the Gene Ontology (GO) categories associated with Protein <some_protein_id> \n\
        ( \n\
            go_gene_product $ontology (protein <some_protein_id>) \n\
        ) \n\
        $ontology \n\
        \n ;Find the Gene Ontology (GO) categories associated with Protein P78415 \n\
        ( \n\
            go_gene_product $ontology (protein P78415) \n\
        ) \n\
        $ontology \n\
        \n ;Find the Gene Ontology (GO) categories associated with Protein O43155 \n\
        ( \n\
            go_gene_product $ontology (protein O43155) \n\
        ) \n\
        $ontology \n\
        \n ;Find the Gene Ontology (GO) categories associated with Protein A6NIX2 \n\
        ( \n\
            go_gene_product $ontology (protein A6NIX2) \n\
        ) \n\
        $ontology \n\
        \n ;Find the Gene Ontology (GO) categories associated with Protein P09769 \n\
        ( \n\
            go_gene_product $ontology (protein P09769) \n\
        ) \n\
        $ontology \n\
        \n ;Find the Gene Ontology (GO) categories associated with Protein Q9NQ38 \n\
        ( \n\
            go_gene_product $ontology (protein Q9NQ38) \n\
        ) \n\
        $ontology \n\
        \n ;Find the  Gene Ontology (GO) categories associated with gene <some_gene_ensembl_id> \n\
        (, \n\
            (transcribed_to (gene <some_gene_ensembl_id>) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
        ) \n\
        $ontology \n\
        \n ;Find the  Gene Ontology (GO) categories associated with gene ENSG00000177508 \n\
        (, \n\
            (transcribed_to (gene ENSG00000177508) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
        ) \n\
        $ontology \n\
        \n ;Find the  Gene Ontology (GO) categories associated with gene ENSG00000164733 \n\
        (, \n\
            (transcribed_to (gene ENSG00000177508) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
        ) \n\
        $ontology \n\
        \n ;Find the Gene Ontology (GO) categories associated with gene <some_gene_HGNC_symbol> (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) <some_gene_HGNC_symbol>) \n\
            (transcribed_to (gene $ens) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
        ) \n\
        $ontology \n\
        \n ;Find the Gene Ontology (GO) categories associated with gene FLRT2 (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) FLRT2) \n\
            (transcribed_to (gene $ens) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
        ) \n\
        $ontology \n\
        \n ;Find the Gene Ontology (GO) categories associated with gene DDX11L1 (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) DDX11L1) \n\
            (transcribed_to (gene $ens) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
        ) \n\
        $ontology \n\
        \n ;Find biological process GO categories associated with gene <some_gene_ensembl_id> \n\
        (, \n\
            (transcribed_to (gene <some_gene_ensembl_id>) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
            (subontology $ontology biological_process) \n\
        ) \n\
        $ontology \n\
         \n ;Find biological process GO categories associated with gene ENSG00000164733 \n\
        (, \n\
            (transcribed_to (gene ENSG00000164733) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
            (subontology $ontology biological_process) \n\
        ) \n\
        $ontology \n\
        \n ;Find biological process Gene Ontology (GO) categories associated with gene <some_gene_HGNC_symbol> (use the gene HGNC symbol instead of ensembl id)\n\
        (, \n\
            (gene_name (gene $ens) <some_gene_HGNC_symbol>) \n\
            (transcribed_to (gene $ens) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
            (subontology $ontology biological_process) \n\
        ) \n\
        $ontology \n\
        \n ;Find biological process Gene Ontology (GO) categories associated with gene DDX11L1 (use the gene HGNC symbol instead of ensembl id)\n\
        (, \n\
            (gene_name (gene $ens) DDX11L1) \n\
            (transcribed_to (gene $ens) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
            (subontology $ontology biological_process) \n\
        ) \n\
        $ontology \n\
        \n ;Find molecular function Gene Ontology (GO) categories associated with gene <some_gene_ensembl_id> \n\
        (, \n\
            (transcribed_to (gene <some_gene_ensembl_id>) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
            (subontology $ontology molecular_function) \n\
        ) \n\
        $ontology \n\
        \n ;Find molecular function Gene Ontology (GO) categories associated with gene ENSG00000164733 \n\
        (, \n\
            (transcribed_to (gene ENSG00000164733) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
            (subontology $ontology molecular_function) \n\
        ) \n\
        $ontology \n\
        \n ;Find molecular function Gene Ontology (GO) categories associated with gene <some_gene_HGNC_symbol> (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) <some_gene_HGNC_symbol>) \n\
            (transcribed_to (gene $ens) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
            (subontology $ontology molecular_function) \n\
        ) \n\
        $ontology \n\
        \n ;Find molecular function Gene Ontology (GO) categories associated with gene DDX11L1 (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) DDX11L1) \n\
            (transcribed_to (gene $ens) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
            (subontology $ontology molecular_function) \n\
        ) \n\
        $ontology \n\
        \n ;Find cellular component Gene Ontology (GO) categories associated with gene <some_gene_HGNC_symbol> (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) <some_gene_HGNC_symbol>) \n\
            (transcribed_to (gene $ens) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
            (subontology $ontology cellular_component) \n\
        ) \n\
        $ontology \n\
        \n ;Find cellular component Gene Ontology (GO) categories associated with gene DDX11L1 (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) DDX11L1) \n\
            (transcribed_to (gene $ens) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
            (subontology $ontology cellular_component) \n\
        ) \n\
        $ontology \n\
        \n ;Find cellular component Gene Ontology (GO) categories associated with gene <some_gene_ensembl_id> \n\
        (, \n\
            (transcribed_to (gene <some_gene_ensembl_id>) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
            (subontology $ontology cellular_component) \n\
        ) \n\
        $ontology \n\
        \n ;Find cellular component Gene Ontology (GO) categories associated with gene ENSG00000164733 \n\
        (, \n\
            (transcribed_to (gene <some_gene_ensembl_id>) $transcript) \n\
            (translates_to $transcript $protein) \n\
            (go_gene_product $ontology $protein) \n\
            (subontology $ontology cellular_component) \n\
        ) \n\
        $ontology \n\
        \n ;What biological process does  ontology term <some_gene_ontology_term_id> represent? \n\
        (, \n\
            (subontology (ontology_term <some_gene_ontology_term_id>) biological_process) \n\
            (term_name (ontology_term <some_gene_ontology_term_id>) $val) \n\
        ) \n\
        $val \n\
        \n\
        \n ;What type of evidence supports the association between the protein identified as <some_protein_id> and the Gene Ontology term <some_gene_ontology_term_id>? \n\
         (evidence (go_gene_product (ontology_term <some_gene_ontology_term_id>) (protein <some_protein_id>)) $val) \n\
         $val \n"
        gene_ontology_edge_query_samples += "*** \n"
        return gene_ontology_edge_query_samples
    
    def generate_sequence_variant_edge_query_samples(self):
        variant_edge_query_samples = self.generate_metta_edge_query_samples()
        variant_edge_query_samples += f"\n Below are some examples of questions and their corresponding query on variants \n***\n\
        \n ;What variants have eqtl association with gene <some_gene_HGNC_symbol> (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) <some_gene_HGNC_symbol>) \n\
            (eqtl $seq (gene $ens)) \n\
        ) \n\
        $seq \n\
        \n ;What variants have eqtl association with gene ARL6IP1 (use the gene HGNC symbol instead of ensembl id) \n\
        (, \n\
            (gene_name (gene $ens) ARL6IP1) \n\
            (eqtl $seq (gene $ens)) \n\
        ) \n\
        $seq \n\
        \n ;What variants have eqtl association with gene <some_gene_ensembl_id> and return the properties of the association \n\
        (, \n\
            (eqtl $seq (gene <some_gene_ensembl_id>)) \n\
            ($prop (eqtl $seq (gene <some_gene_ensembl_id>)) $val) \n\
        ) \n\
            ($prop (eqtl $seq (gene <some_gene_ensembl_id>)) $val) \n\
        \n ;What variants have eqtl association with gene ENSG00000161980 and return the properties of the association \n\
        (, \n\
            (eqtl $seq (gene ENSG00000161980)) \n\
            ($prop (eqtl $seq (gene ENSG00000161980)) $val) \n\
        ) \n\
            ($prop (eqtl $seq (gene ENSG00000161980)) $val) \n\
        \n ;What variants have eqtl association with gene <some_gene_HGNC_symbol> (use the gene HGNC symbol instead of ensembl id) and return the properties of the association \n\
        (, \n\
            (gene_name (gene $ens) <some_gene_HGNC_symbol>) \n\
            (eqtl $seq $ens) \n\
            ($prop (eqtl $seq (gene $ens)) $val) \n\
        ) \n\
        ($prop (eqtl $seq (gene $ens)) $val) \n\
        \n ;What variants have eqtl association with gene IRX3 (use the gene HGNC symbol instead of ensembl id) and return the properties of the association \n\
        (, \n\
            (gene_name (gene $ens) IRX3) \n\
            (eqtl $seq $ens) \n\
            ($prop (eqtl $seq (gene $ens)) $val) \n\
        ) \n\
        ($prop (eqtl $seq (gene $ens)) $val) \n\
        \n  ;Get the properties of the eqtl association involving the <some_sequence_variant_id> variant and the gene <some_gene_ensembl_id> \n\
        (, \n\
            ($prop (eqtl  (sequence_variant <some_sequence_variant_id>) (gene <some_gene_ensembl_id>)) $val) \n\
        ) \n\
        ($prop (eqtl (sequence_variant <some_sequence_variant_id>) (gene <some_gene_ensembl_id>)) $val) \n\
        \n  ;Get the properties of the eqtl association involving the rs224167 variant and the gene ENSG00000234769 \n\
        (, \n\
            ($prop (eqtl  (sequence_variant rs224167) (gene ENSG00000234769)) $val) \n\
        ) \n\
        ($prop (eqtl (sequence_variant rs224167) (gene ENSG00000234769)) $val) \n\
        \n ;Get the slope of the eqtl association involving the <some_sequence_variant_id> variant and the gene <some_gene_ensembl_id> \n\
        (, \n\
            (slope (eqtl  (sequence_variant <some_sequence_variant_id>) (gene <some_gene_ensembl_id>)) $val) \n\
        ) \n\
        (slope (eqtl (sequence_variant <some_sequence_variant_id>) (gene <some_gene_ensembl_id>)) $val) \n\
        \n ;Get the slope of the eqtl association involving the rs224167 variant and the gene ENSG00000234769 \n\
        (, \n\
            (slope (eqtl  (sequence_variant rs224167) (gene ENSG00000234769)) $val) \n\
        ) \n\
        (slope (eqtl (sequence_variant rs224167) (gene ENSG00000234769)) $val) \n\
        \n ;Get the p-value of the eqtl association involving the <some_sequence_variant_id> variant and the gene <some_gene_ensembl_id> \n\
            (, \n\
                (p_value (eqtl (sequence_variant <some_sequence_variant_id>) (gene <some_gene_ensembl_id>)) $val) \n\
            ) \n\
            (p_value (eqtl (sequence_variant <some_sequence_variant_id>) (gene <some_gene_ensembl_id>)) $val) \n\
        ) \n\
        \n ;Get the p-value of the eqtl association involving the rs2239739 variant and the gene ENSG00000167930 \n\
            (, \n\
                (p_value (eqtl (sequence_variant rs2239739) (gene ENSG00000167930) $val) \n\
            ) \n\
            (p_value (eqtl (sequence_variant rs2239739) (gene ENSG00000167930)) $val) \n\
        ) \n\
        \n ;Get the biological context of the eqtl association involving the <some_sequence_variant_id> variant and the gene <some_gene_ensembl_id> \n\
        (, \n\
            (biological_context (eqtl (sequence_variant <some_sequence_variant_id>) (gene <some_gene_ensembl_id>)) $val) \n\
        ) \n\
        (biological_context (eqtl (sequence_variant <some_sequence_variant_id>) (gene <some_gene_ensembl_id>)) $val) \n\
        \n ;Get the biological context of the eqtl association involving the rs2239739 variant and the gene ENSG00000167930 \n\
        (, \n\
            (biological_context (eqtl (sequence_variant rs2239739) (gene ENSG00000167930)) $val) \n\
        ) \n\
        (biological_context (eqtl (sequence_variant rs2239739) (gene ENSG00000167930)) $val) \n\
        \n ;What genes have eqtl association with  variant <some_sequence_variant_id>, return the properties of the association \n\
        (, \n\
            (eqtl (sequence_variant <some_sequence_variant_id>)  $ens) \n\
            ($prop (eqtl (sequence_variant <some_sequence_variant_id>) $ens) $val) \n\
        ) \n\
        ($prop (eqtl (sequence_variant <some_sequence_variant_id>) $ens) $val) \n\
        \n ;What genes have eqtl association with  variant rs2239739, return the properties of the association \n\
        (, \n\
            (eqtl (sequence_variant rs2239739)  $ens) \n\
            ($prop (eqtl (sequence_variant rs2239739) $ens) $val) \n\
        ) \n\
        ($prop (eqtl (sequence_variant rs2239739) $ens) $val) \n"
        variant_edge_query_samples += "*** \n"
        return variant_edge_query_samples

    def generate_protein_edge_query_samples(self):
        protein_edge_query_samples = self.generate_metta_edge_query_samples()
        protein_edge_query_samples += f"\n Below are some examples of questions and their corresponding query on proteins \n***\n\
        \n ;Find the Gene Ontology (GO) categories associated with protein <some_protein_id> \n\
        \n ( \n\
            go_gene_product $ontology (protein <some_protein_id>) \n\
        ) \n\
        $ontology \n\
        \n ;Find the Gene Ontology (GO) categories associated with protein P78415 \n\
        \n ( \n\
            go_gene_product $ontology (protein P78415) \n\
        ) \n\
        $ontology \n\
        \n ;Find the Gene Ontology (GO) categories associated with protein O43155 \n\
        \n ( \n\
            go_gene_product $ontology (protein O43155) \n\
        ) \n\
        $ontology \n\
        \n ;What are the proteins that gene <some_gene_ensembl_id> codes for \n\
        \n (, \n\
            (transcribed_to (gene <some_gene_ensembl_id>) $transcript) \n\
            (translates_to $transcript $protein) \n\
        ) \n\
        $protein \n\
        \n ;What are the proteins that gene ENSG00000052795 codes for \n\
        \n (, \n\
            (transcribed_to (gene ENSG00000052795) $transcript) \n\
            (translates_to $transcript $protein) \n\
        ) \n\
        $protein \n\
        \n ;What are the proteins that gene <some_gene_HGNC_symbol> codes for (use the gene HGNC symbol instead of ensembl id)\n\
        \n (, \n\
            (gene_name (gene $ens) <some_gene_HGNC_symbol>) \n\
            (transcribed_to (gene $ens) $transcript) \n\
            (translates_to $transcript $protein) \n\
        ) \n\
        \n ;What are the proteins that gene HBA1 codes for (use the gene HGNC symbol instead of ensembl id)\n\
        \n (, \n\
            (gene_name (gene $ens) HBA1) \n\
            (transcribed_to (gene $ens) $transcript) \n\
            (translates_to $transcript $protein) \n\
        ) \n\
        $protein \n\
        \n ;What type of evidence supports the association between the protein identified as <some_protein_id> and the Gene Ontology term <some_gene_ontology_term_id>? \n\
        \n (evidence (go_gene_product (ontology_term <some_gene_ontology_term_id>) (protein <some_protein_id>)) $val) \n\
        $val \n"
        protein_edge_query_samples += "*** \n"
        return protein_edge_query_samples


    def get_metta_prompt(self) -> str:

        metta_node_samples = self.generate_metta_node_samples()
        metta_edge_samples = self.generate_metta_edge_samples()

        node_keys = self.schema_nodes.keys()

        metta_node_query_samples = self.generate_metta_node_query_samples()
        if "protein" in node_keys:
            metta_edge_query_samples = self.generate_protein_edge_query_samples()
        elif "transcript" in node_keys:
            metta_edge_query_samples = self.generate_transcripts_edge_query_samples()
        elif "ontology_term" in node_keys:
            metta_edge_query_samples = self.generate_gene_ontology_edge_query_samples()
        elif "pathway" in node_keys:
            metta_edge_query_samples = self.generate_pathway_edge_query_samples()
        elif "sequence_variant" in node_keys:
            metta_edge_query_samples = self.generate_sequence_variant_edge_query_samples()
        else:
            metta_edge_query_samples = self.generate_metta_edge_query_samples()
        print(metta_node_query_samples)
        print(metta_edge_query_samples)
        prompt = (
            f"I have a dataset for storing biology data using a lisp style syntax."
            f"The dataset is classified into 'nodes' and 'edges' as follows:"
            f"{metta_node_samples}\n"
            f"{metta_edge_samples}\n"

            f"You will generate Scheme-like queries for this dataset that will answer the user's question."
            f"The query will have two outer parenthesis. The first one will contain the pattern matching query\
                on the dataset, and the second one will contain the variables to be returned by the query."
            f"You can refer to the following examples for constructing the queries:"
            f"{metta_node_query_samples}\n"
            f"{metta_edge_query_samples}\n"
            
            f"<some_gene_HGNC_symbol> is a gene name like 'HBM', 'FLRT2' and <some_gene_ensembl_id> is an ensembl id like 'ENSG00000170540', 'ENSG00000161980'. A gene has two of them and which one to use will be mentioned in the user's question."
            f"For example, 'gene <some_gene_ensembl_id>' can be like 'gene ENSG00000170540', 'gene <some_gene_HGNC_symbol>' can be like 'gene FLRT2' and for sequence varaint, 'sequence_variant <some_sequence_variant_id>' can be like 'sequence_variant rs2239739'."
            f"If the ensembl id(like 'ENSG00000170540') is given in the user's question, don't write something like '(gene ENSG00000186790 $ens)' or '(gene_name (gene $ens) ENSG00000186790)'. Instead, just use the ensemble id in the subsequent statements."
            f"Let me give you two examples that show where you need to write '(gene_name (gene $ens) <some_gene_HGNC_symbol>)'. If the user's question contains an HGNC symbol, you have to first retrieve the Ensembl ID. Below is an example that demonstrates that:\
            \n ;What are the proteins that gene <some_gene_HGNC_symbol> codes for (use the gene HGNC symbol instead of ensembl id)\n\
            (, \n\
                (gene_name (gene $ens) <some_gene_HGNC_symbol>) \n\
                (transcribed_to (gene $ens) $transcript) \n\
                (translates_to $transcript $protein) \n\
            ) \n\
            In the above example, since the user's question describes a gene with the gene's HGNC symbol (examples of HGNC symbols are 'HBM', 'FLRT2'), the gene's Ensembl ID needs to be retrieved first. '(gene_name (gene $ens) <some_gene_HGNC_symbol>)' retrieves the gene's Ensembl ID. \n\
            In another case, let's consider the example below: \n\
            \n ;What are the proteins that gene <some_gene_ensembl_id> codes for\n\
            (, \n\
                (transcribed_to (gene <some_gene_ensembl_id>) $transcript) \n\
                (translates_to $transcript $protein) \n\
            )\
            Since the user's question described the gene with the gene's Ensembl ID, there is no need to retrieve the Ensembl ID as it is already given in the user's question. The Ensembl ID is directly used in the subsequent statement. In addition, whether to use HGNC symbol or Ensembl ID will be stated in the user's question."
            f"Example queries that are given above contain both complex and simple queries. Examples that start with ',' are complex queries those that don't contains ',' are simple queries."
            f"Complex queries propagate variable values through expression from the top to the bottom. for example let's look at the below complex query\n\
                (,\n\
                        (gene_name (gene $ens) <some_gene_HGNC_symbol>)\n\
                        (transcribed_to (gene $ens) $transcript)\n\
                        (translates_to $transcript $protein)\n\
                        (go_gene_product $ontology $protein)\n\
                        (subontology $ontology <some_subontology_val>)\n\
                )\n\
                ($ontology)\n\
            from '(gene_name (gene $ens) <some_gene_HGNC_symbol>)' expression, the value $ens will be retrived and will be passed to '(transcribed_to (gene $ens) $transcript)'.\
            The same way, from '(transcribed_to (gene $ens) $transcript)' the value of $transcript will be retrived and will be passed to '(translates_to $transcript $protein)'.\
            Again, from '(translates_to $transcript $protein)' $protien will be retrieved and will be passed to '(go_gene_product $ontology $protein)'.\
            Finally, from '(go_gene_product $ontology $protein)', $ontology will be retrieved and will be passed to '(subontology $ontology <some_subontology_val>)'. At the end value of $ontology will be returned."
            f"Simple queries just pattern match a single experession and then return the result. Let's look at one example\n\
                ( \n\
                    (go_gene_product $ontology (protein <some_protein_id>)) \n\
                ) \n\
                $ontology \n\
                \n\
            The above example just pattern match the given expression and return the value of $ontology."
            f"Everything between the three hashtags (### .... ###) is the exact format of the dataset."
            f"Everything between the three asterisks (*** .... ***) is a query."
            f"Everything between angle brackets (<..>) is a variable that should either be replaced with the appropriate\
                'id' or 'value' found in the user's question or should be replaced with a vairable to be returned by the query."\
            f"For example, let's look at some user questions and their corresponding query.\
                'Give the description for the ontology term with ID 'GO:0000785''.\
            for the above user question, the below query can be generated\n\
                ( \n\
                    (description (ontology_term GO:0000785) $val) \n\
                ) \n\
                $val\n\
            let's look at other user question that requires complex query to be genrated.\
            'Find all properties of genes that belong into biological process subontology.'\n\
            (,\n\
                (subontology (ontology_term $id) biological_process)\n\
                ($prop (ontology_term $id) $val)\n\
            )\n\
                ($prop $val)\n\
            "
            f"The word after the dollar sign ($) is a variable that can replace values that aren't provided by the user or\
                unknown values that are requested by the user."
            f"The 'id' or 'value' you find in the user's question should be treated as symbols and must not be wrapped in quotes."
            f"Return only query,  no explanation and other texts"
            f"Based on the information given to you above, you will write a pattern matching query on the dataset for the user's question."
        )
        return prompt
    