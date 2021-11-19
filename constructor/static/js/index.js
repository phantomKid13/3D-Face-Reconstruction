if (window.history.replaceState){
    window.history.replaceState( null, null, window.location.href );
}

// File Upload
function removeUpload(){
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
}

function readURL(input){

    if (input.files && input.files[0]){
  
      var reader = new FileReader();
  
      reader.onload = function(e) {
        $('.image-upload-wrap').hide();
        $('.file-upload-image').attr('src', e.target.result);
        $('.file-upload-content').show();
        $('.image-title').html(input.files[0].name);
      };
  
      reader.readAsDataURL(input.files[0]);
      
    } 
    else {
        removeUpload();
    }
    
}

// $('.image-upload-wrap').bind('dragover', function(){
//     $('.image-upload-wrap').addClass('image-dropping');
// });

// $('.image-upload-wrap').bind('dragleave', function () {
//     $('.image-upload-wrap').removeClass('image-dropping');
// });
  
// Toggle Blocks
function runUpload(){

    $('input[type="button"][value="File Upload"]').css("background","#40054a")
    $('input[type="button"][value="Camera"]').css("background","#591fb2")
    $('input[type="button"][value="Meshlab"]').css("background","#591fb2")

    $.ajax({
        url: 'upload', 
        success: function(data) {
            $('.file-upload').css("display","block");
            $('#cam').css("display","none");
            $('#lab').css("display","none");
        } 
    });
}

function runCam(){

    $('input[type="button"][value="File Upload"]').css("background","#591fb2")
    $('input[type="button"][value="Camera"]').css("background","#40054a")
    $('input[type="button"][value="Meshlab"]').css("background","#591fb2")

    $.ajax({
        url: 'cam', 
        success: function(data) {
            $('#cam').css("display","block");
            $('.file-upload').css("display","none");
            $('#lab').css("display","none");
        }
    });
}

function runLab(){

    $('input[type="button"][value="File Upload"]').css("background","#591fb2")
    $('input[type="button"][value="Camera"]').css("background","#591fb2")
    $('input[type="button"][value="Meshlab"]').css("background","#40054a")

    $.ajax({
        url: 'lab', 
        success: function(data) {
            $('#cam').css("display","none");
            $('.file-upload').css("display","none");
            $('#lab').css("display","block");
        }
    });
}

(function ($) {
    "use strict";
    var mainApp = {

        main_fun: function(){
            /*====================================
             CUSTOM LINKS SCROLLING FUNCTION 
            ======================================*/

            $('a[href*=#]').click(function(){
                if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
               && location.hostname == this.hostname) {
                    var $target = $(this.hash);
                    $target = $target.length && $target
                    || $('[name=' + this.hash.slice(1) + ']');
                    if ($target.length) {
                        var targetOffset = $target.offset().top;
                        $('html,body')
                        .animate({ scrollTop: targetOffset }, 800); //set scroll speed here
                        return false;
                    }
                }
            });
        
            /*====================================
               WRITE YOUR SCRIPTS BELOW 
           ======================================*/
        },

        initialization: function(){
            mainApp.main_fun();
        }
    }
    // Initializing ///

    $(document).ready(function(){
        mainApp.main_fun();
    });

}(jQuery));



