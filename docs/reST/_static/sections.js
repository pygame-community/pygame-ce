function toggleSectionVisibility(section, message){
	document.getElementById(section).hidden = ! document.getElementById(section).hidden;
	if (document.getElementById(section).hidden === true){ // show
		items = localStorage.getItem('hidden');
		if (items !== null){
			if (!(items.includes(section))){
				items = items + section + '|';
			}
			localStorage.setItem('hidden', items);
		} else {
			localStorage.setItem('hidden', section + '|');
		}
		document.getElementById(section[0]).innerHTML = document.getElementById(section[0]).innerHTML.replace('▼', '▲');
	} else {  // hide
		items = localStorage.getItem('hidden');
		if (items !== null){
			if (items.includes(section)){
				items = items.replace(section + '|', '');
			}
			localStorage.setItem('hidden', items);
		}
		document.getElementById(section[0]).innerHTML = document.getElementById(section[0]).innerHTML.replace('▲', '▼');
	}
}

function toggleChecked(classname){
    if (window.innerWidth <= 1100) {
        el = document.getElementsByClassName(classname)[0];
        console.log(el.id);
        if (el.id !== 'clicked') {
            el.id = 'clicked';
            htmlElement.classList.add('clicked');
        } else {
            el.id = null;
            htmlElement.classList.remove('clicked');
        }
    }
}