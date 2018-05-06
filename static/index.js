// create dropdown from Flask API
var url = "/names";
Plotly.d3.json(url, function(error, response) {
    if (error) throw error;
    var $dropDown = document.getElementById("selDataset")
    for (var i=0; i< response.length; i++){
        var $optionChoice = document.createElement("option");
        $optionChoice.innerHTML = response[i];
        $optionChoice.value = response[i];
        $dropDown.appendChild($optionChoice);
    }
});

// set intial sample value as "BB_940"
var defaultSample = "BB_940"
function init(sample){
    Plotly.d3.json("/metadata/" + sample, function(error, response){
        if (error) throw error;
        var responseKeys = Object.keys(response);
        var $sampleInfoPanel = document.querySelector("#sample-metadata");
        $sampleInfoPanel.innerHTML = null;
        for (var i=0; i<responseKeys.length; i++){
            var $sample = document.createElement('p');
            $sample.innerHTML = responseKeys[i] + ": " + response[responseKeys[i]];
            $sampleInfoPanel.appendChild($sample)
        };
    });

}

init(defaultSample);