// Script for Select All Checkboxes
function toggle() 
{
  checkboxes = document.getElementsByClassName('check-box');
  len = checkboxes.length;
  select_all = document.getElementById('select-all');
  if (select_all.checked == true) 
  {
    for (let i = 0; i < len; i++) 
    {
      const checkbox = checkboxes[i];
      checkbox.checked = true;
    }
  }
  else 
  {
    for (let i = 0; i < len; i++) 
    {
      const checkbox = checkboxes[i];
      checkbox.checked = false;
    }
  }
}