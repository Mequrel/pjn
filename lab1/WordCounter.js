var fs = require('fs');

var filename = process.argv[2];

fs.readFile(filename, 'utf8', function (err,data) {
  var words = data.split(/[ \t\r\n\v\f!"#$%&'()*+,\-.\/:;<=>?\[\\\]^_`{|}~]+/);
  var occurences = {};

  for(i in words) {
    var word = words[i].toLowerCase();
 
    if(word in occurences) {
      occurences[word]++
    }
    else {
      occurences[word] = 1;
    }
  }

  var sortable = [];
  for (var word in occurences)
        sortable.push([word, occurences[word]])
  sortable.sort(function(a, b) {return b[1] - a[1]})

  for(i in sortable) {
    console.log(sortable[i][0] + " " + sortable[i][1])
  }
  
});