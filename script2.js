document.addEventListener('DOMContentLoaded', () => {
    function createParagraph() {
      const para = document.getElementById('functionality');
      para.textContent = 'No Functionality Yet! Nice try though!';
  
    }
  
    function openDataWindow() { 
      window.open('BathymetryML.html', "_self");
    }
  
    function openFileWindow() { 
      window.open('dragAndDrop.html', "_self");
    }

    function openTestWindow() { 
        window.open('testPage.html', "_self");
      }
    function openOutputWindow() {
        window.open('outputPage.html', "_self");
    }


  
    const buttonOne = document.querySelector('#dataclean');
    buttonOne.addEventListener('click', openDataWindow);
  
    const buttonTwo = document.querySelector('#modelTrain');
    buttonTwo.addEventListener('click', openFileWindow);
  
    const buttonThree = document.querySelector('#testData');
    buttonThree.addEventListener('click', openTestWindow);
  
    const buttonFour = document.querySelector('#outputProfile');
    buttonFour.addEventListener('click', openOutputWindow);
  
  });