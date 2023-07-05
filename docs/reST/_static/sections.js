function toggleSectionVisibility(section){
    document.getElementById(section).hidden = ! document.getElementById(section).hidden;
    if (document.getElementById(section).hidden === true){ // show
        items = sessionStorage.getItem('hidden');
        if (items !== null){
            if (!(items.includes(section))){
                items = items + section + '|';
            }
            sessionStorage.setItem('hidden', items);
            } else {
                sessionStorage.setItem('hidden', section + '|');
            }
            document.getElementById(section[0]).innerHTML = document.getElementById(section[0]).innerHTML.replace('▼', '▲');
    } else {  // hide
        items = sessionStorage.getItem('hidden');
        if (items !== null){
            if (items.includes(section)){
                items = items.replace(section + '|', '');
            }
            sessionStorage.setItem('hidden', items);
        }
        document.getElementById(section[0]).innerHTML = document.getElementById(section[0]).innerHTML.replace('▲', '▼');
    }
}

function toggleChecked(classname){
    if (window.innerWidth <= 1100) {
        el = document.getElementsByClassName(classname)[0];
        if (el.id !== 'clicked') {
            el.id = 'clicked';
            htmlElement.classList.add('clicked');
        } else {
            el.id = null;
            htmlElement.classList.remove('clicked');
        }
    }
}
