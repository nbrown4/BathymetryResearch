document.addEventListener('DOMContentLoaded', () => {
    function createParagraph() {
      const para = document.getElementById('functionality');
      para.textContent = 'No Functionality Yet! Nice try though!';
  
    }
  
    function openDataWindow() { 
      window.location.href = '../BathymetryML'
    }
  
    function openFileWindow() { 
      window.location.href = '../../dragAndDrop'
    }
  
    function openTestWindow() { 
      window.location.href = '../../testPage'
      }
  
    function openOutputWindow() { 
        window.location.href = '../../outputPage'
      }

    function runPython(){
      
      const {PythonShell} = require('python-shell');
  
      let pyshell = new PythonShell('script.py');
  
      pyshell.on('message', function(message) {
          console.log(message);
      })
  
      pyshell.end(function (err) {
          if (err){
              throw err;
          };
          console.log('finished');
      });
    }

  
  
    const buttonOne = document.querySelector('#dataclean');
    buttonOne.addEventListener('click', openDataWindow);

    const buttonTwo = document.querySelector('#modelTrain');
    buttonTwo.addEventListener('click', openFileWindow);
  
    const buttonThree = document.querySelector('#testData');
    buttonThree.addEventListener('click', openTestWindow);
  
    const buttonFour = document.querySelector('#outputProfile');
    buttonFour.addEventListener('click', openOutputWindow);

    const buttonFive = document.querySelector('#runTheTest');
    buttonFive.addEventListener('click', runPython);

  
  });
