from flask import Flask
from flask import render_template
import daru
import json
import operator

app = Flask(__name__)

def json_response(json_string):
    response = app.response_class(
        response=json_string,
        status=200,
        mimetype='application/json'
    )

    return response

@app.route("/api/patches/")
def patches():

    num_patches = 200

    indices = daru.read_index("daru.idaru")
    metric_sorted = sorted(indices.items(), key=operator.itemgetter(1), reverse=True)
    top_indices = metric_sorted[:num_patches:]

    to_json = dict(top_indices)

    json_string = json.dumps(to_json)

    return json_response(json_string)

@app.route("/api/patch/<patch_id>")
def records(patch_id):
    record_list = daru.read_patch("daru.daru", int(patch_id))

    return records_to_json(record_list)


def records_to_json(records):
    record_dicts = []
    for record in records:
        record_dict = {
            "day"  : record.day,
            "qname": record.qname,
            "flags": record.flags,
            "rname": record.rname,
            "pos"  : record.pos,
            "mapq" : record.mapq,
            "cigar": record.cigar,
            "seq"  : record.seq,
            "qual" : record.qual
        }
        record_dicts.append(record_dict)

    json_string = json.dumps(record_dicts)

    return json_response(json_string)

@app.route("/")
def root():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
