import csv
import argparse
import sqlite3

def build_sql_db_mapping(db_mapping_fp, out_fp, id_col, gene_col, taxa_col):
    conn = sqlite3.connect(out_fp)
    c = conn.cursor()

    # if the table doesn't exist in the database create it
    if not conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mapping'").fetchone():
        c.execute("CREATE TABLE mapping (gene text, function text, taxid text)")
    else:
        sys.exit("Table already exists in the database. If you would like to rebuild it please delete and run again.")

    with open(db_mapping_fp, 'r') as f_in:
        reader = csv.reader(f_in, delimiter='\t') # initialize the csv reader
        
        header = reader.next()
        id_idx = header.index(id_col)
        gene_idx = header.index(gene_col)
        taxa_idx = header.index(taxa_col)

        # fill in the database from the text file
        for line in reader:
            c.execute("INSERT INTO mapping VALUES ('%s', '%s', '%s')" % (line[id_idx], line[gene_idx], line[taxa_idx]))
    conn.commit()
    conn.close()

def build_mapping_db(argv=None):
    parser = argparse.ArgumentParser(description="Aggregates alignment results to gene function and taxonomy.")
    
    parser.add_argument(
        "--db-mapping-fp", required=True,
        #type=argparse.FileType("r"), 
        help="Sequence ID to gene funtion and taxonomy association file")
    parser.add_argument(
        "--mapping-sql-fp", required=True,
        help="Output sequel db filepath")
    parser.add_argument(
        "--id-col", required=False,
        default="Subject",
        help="Column name for the sequence IDs of the database (default: %(default)s)")
    parser.add_argument(
        "--gene-col", required=False,
        default="gene_name",
        help="Column name for the gene function in the database (default: %(default)s)")
    parser.add_argument(
        "--taxa-col", required=False,
        default="taxid",
        help="Column name for the ncbi ID of the database sequence (default: %(default)s)")
    args = parser.parse_args(argv)
    
    build_sql_db_mapping(args.db_mapping_fp, args.mapping_sql_fp, args.id_col, args.gene_col, args.taxa_col)

