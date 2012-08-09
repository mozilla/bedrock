///DOC READY FUNCTIONS
$(document).ready(function() {

if ($('#sidebar nav ul')[0]){

  $('#sidebar nav ul').find('a').click(function(e){ //Click function to toggle extending lists
    e.preventDefault();
    $(this).next().slideToggle('fast').css('zoom', '1'); //Find the next element after the clicked element
    $(this).parent('li').toggleClass('collapse'); //Add a class for styling
  });

  $('#sidebar nav ul > li').each(function(){ //Function initially hide lists with the override class of "extended"
    if (!$(this).hasClass('extended')){
     $(this).find('ul').slideUp('fast').css('zoom', '1'); //hide all lists without a parent of "extended"
     $(this).toggleClass('collapse'); //Add a class for styling
    }

  });

}

});
