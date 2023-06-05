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
		document.getElementById(section[0]).innerHTML = document.getElementById(section[0]).innerHTML.replace('▼', '▲')
	} else {  // hide
		items = localStorage.getItem('hidden');
		if (items !== null){
			if (items.includes(section)){
				items = items.replace(section + '|', '')
			}
			localStorage.setItem('hidden', items);
		}
		document.getElementById(section[0]).innerHTML = document.getElementById(section[0]).innerHTML.replace('▲', '▼')
	}
}