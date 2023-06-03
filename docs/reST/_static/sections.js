function toggleSectionVisibility(section){
	document.getElementById(section).hidden = ! document.getElementById(section).hidden;
	if (document.getElementById(section).hidden === true){
		items = localStorage.getItem('hidden');
		if (items !== null){
			if (!(items.includes(section))){
				items = items + '|' + section + '|';
			}
			localStorage.setItem('hidden', items);
		} else {
			localStorage.setItem('hidden', section);
		}
	} else {
		items = localStorage.getItem('hidden');
		if (items !== null){
			if (items.includes(section)){
				items = items.replace(section + '|', '')
			}
			localStorage.setItem('hidden', items);
		}
	}
}