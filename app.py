# dependencies
from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine, desc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

#  Flask set up
app = Flask(__name__)

engine = create_engine("sqlite:///DataSets/belly_button_biodiversity.sqlite", echo=False)

Base = automap_base()

Base.prepare(engine, reflect=True)

# References to the table
OTU = Base.classes.otu
Samples_metadata = Base.classes.samples_metadata
Samples = Base.classes.samples

# Create the session
session = Session(engine)

# Create API routes
# Return the dashboard homepage
@app.route("/")
def index():
    return render_template("index.html")

# Return a list of sample names
@app.route("/names")
def names():
    sample_names = Samples.__table__.columns.keys()
    samples = sample_names[1:]
    return (jsonify(samples))

# Return a list of OTU descriptions
@app.route("/otu")
def otu():
    OTU_descriptions = session.query(OTU.lowest_taxonomic_unit_found).all()
    otu_ids = [i for i, in OTU_descriptions]
    return (jsonify(otu_ids))

@app.route("/otu_descriptions")
def otu_descriptions():
    otu_descriptions = session.query(OTU.otu_id, OTU.lowest_taxonomic_unit_found).all()
    otu_dict = {}
    for row in otu_descriptions:
        otu_dict[row[0]] = row[1]
    return jsonify(otu_dict)

# Return a json dictionary of sample metadata
@app.route("/metadata/<sample>")
def sample_metadata(sample):
    sample_name = sample.replace("BB_", "")
    sample_metadata = session.query(Samples_metadata.AGE, Samples_metadata.BBTYPE, Samples_metadata.ETHNICITY, Samples_metadata.GENDER, Samples_metadata.LOCATION, Samples_metadata.SAMPLEID).filter_by(SAMPLEID = sample_name).all()
    sample_data = sample_metadata[0]
    sample_data_dict = {"AGE": sample_data[0],"BBTYPE": sample_data[1],"ETHNICITY": sample_data[2],"GENDER": sample_data[3],"LOCATION": sample_data[4],"SAMPLEID": sample_data[5]
    }
    return jsonify(sample_data_dict)

# Returns an integer value for the weekly washing frequency `WFREQ`
@app.route('/wfreq/<sample>')
def wfreq(sample):
    wfreq = session.query(Samples_metadata.WFREQ).filter(Samples_metadata.SAMPLEID==sample[3:]).all()
    return jsonify(wfreq[0][0])

# Return a list of dictionaries containing sorted lists  for `otu_ids` and `sample_values`
@app.route('/samples/<sample>')
def samples(sample):
    sample_query = "Samples." + sample
    result = session.query(Samples.otu_id, sample_query).order_by(desc(sample_query)).all()
    otu_ids = [result[x][0] for x in range(len(result))]   
    sample_values = [result[x][1] for x in range(len(result))]
    dict_list = [{"otu_ids": otu_ids}, {"sample_values": sample_values}]
    return jsonify(dict_list)

if __name__ == '__main__':
    app.run(debug=True)
