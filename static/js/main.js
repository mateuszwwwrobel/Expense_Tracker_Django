
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
    else if(document.title == 'Profile - Expense Tracker'){
        let element = document.getElementById('nav-profile')
        element.className += ' nav-button-active'
    }
};


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
         }
        }
    }
    return cookieValue;
}


function DeleteExpense(expense_id) {
    const csrftoken = getCookie('csrftoken');

    fetch('/expenses/delete/' + expense_id, {
        method: 'DELETE',
        headers: {
                    'Content-Type':'application/json',
                    'X-CSRFTOKEN': csrftoken
                },
    }).then(response => response)
        .then(data => {
            location.reload();
        })
        .catch(error => {
            console.log(error)
        })
}
