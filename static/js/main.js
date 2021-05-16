
navbarSelector()


function navbarSelector() {
    if (document.title == 'About - Expense Tracker'){
        let element = document.getElementById('nav-about')
        element.className += ' nav-button-active'
    }
    else if(document.title == 'Contact - Expense Tracker'){
        let element = document.getElementById('nav-contact')
        element.className += ' nav-button-active'
    }
};

