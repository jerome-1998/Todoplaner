'use strict'


$(document).ready( function(){
    // Aufgaben hinzufügen
    $(document).on('click', '.add', function(){
        let quest_text = $('#add_quest_text').val();
        let quest_art = $('#quest_art').children('option:selected').val();
        $.ajax({
            type: 'POST',
            url: '/add',
            data: {quest_text: quest_text, quest_art: quest_art},
            success: function(data){
                let rows = $(data).filter('.questList');
                $('#add_quest_text').val('');
                return $('.questList').html(rows);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                alert("error: "+ errorThrown);
            }
        });
    });
    // Aufgaben löschen
    $(document).on('click', '.delete', function(){
        let id = $(this).attr('id');
        $.ajax({
            type: 'POST',
            url: '/delete',
            data: {qid: id},
            success: function(data){
                let rows = $(data).filter('.questList');
                return $('.questList').html(rows);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                alert("error: "+ errorThrown);
            }
        });
    });
    // Aufgaben abhaken
    $(document).on('click', '.check',function(){
        let id = $(this).attr('id');
        $.ajax({
            type: 'POST',
            url: '/update',
            data: {qid :id},
            success: function(data){
                let rows = $(data).filter('.questList');
                return $('.questList').html(rows);
            },
            error:function(XMLHttpRequest, textStatus, errorThrown){
                alert("error: "+errorThrown);
            }
        });
    });
    // Aufgaben sortieren
    $(document).on('click', '.sort', function(){
        let url = $(this).attr('id');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(data){
                let rows = $(data).filter('.questList');
                return $('.questList').html(rows);
            },
            error:function (XMLHttpRequest, textStatus, errorThrown){
                alert("error: "+ errorThrown);
            }
        });
    });
    // Aufgaben filtern
    $('a').click(function(){
        let url = $(this).attr('id');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(data){
                let rows = $(data).filter('.questList');
                return $('.questList').html(rows);
            },
            error:function (XMLHttpRequest, textStatus, errorThrown){
                alert("error: "+ errorThrown);
            }           
        });
    });
});