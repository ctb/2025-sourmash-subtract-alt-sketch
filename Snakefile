rule gather_round2:
    input:
        query="SRR606249.round2.sig.zip",
        db="podar-ref.zip",
    output:
        "SRR606249.x.podar-ref.round2.k21.csv",
    shell: """
       sourmash scripts fastgather {input.query} {input.db} -k 21 --scaled 1000 -o {output}
    """

rule sub:
    input:
        script="./sub.py",
        query="SRR606249.abundtrim.sig",
        db="podar-ref.zip",
        gather="SRR606249.x.podar-ref.k51.csv",
    output:
        "SRR606249.round2.sig.zip",
    shell: """
        {input.script} {input.query} {input.db} -m DNA -k 21 -o {output} \
            --picklist {input.gather}:match_name:ident
    """

rule gather_round1:
    input:
        query="SRR606249.abundtrim.sig",
        db="podar-ref.zip",
    output:
        "SRR606249.x.podar-ref.k51.csv",
    shell: """
       sourmash scripts fastgather {input.query} {input.db} -k 51 --scaled 100_000 -o {output}
    """

