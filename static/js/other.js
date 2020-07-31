function loadartist(){
    // var artist_name=document.getElementById('artist_name').innerHTML
    // alert(artist_name)
    $.get("/albums-store/",function(data,status){
        alert("success")
        $('#single_artist').val('');
        for(var s in data){
            // $('#para').append(s);
            $('#single_artist').append(
                '<div class="col-12 col-sm-4 col-md-3 col-lg-2 single-album-item t c p">'+
                    '<div class="single-album">'+
                        '<img style="height: 200px;width: 200px;" src="/media/'+data[s]+'" alt="">'+
                        '<div class="album-info">'+
                            '<a href="/albums-store/'+s+'" >'+
                                '<h5>'s'</h5>'+
                            '</a>'+
                            
                        '</div>'+
                    '</div>'+
                '</div>'
            )

        }
        
    })
  };
/*<script type="text/javascript">
    var myAudio=document.getElementById('audio')
    myAudio.oncanplaythrough=function(){this.play();}
</script> 
*/
// $("audio").on("play", function() {
//     var id = $(this).attr('id');

//     $("audio").not(this).each(function(index, audio) {
//         audio.pause();
//     });
// });
var audioOne = document.querySelector('#audio-1');
var audioTwo = document.querySelector('#audio-2');

var allAudios = document.querySelectorAll('audio');

function stopAllAudio(){
	allAudios.forEach(function(audio){
		audio.pause();
	});
}

document.querySelector('#play-1').addEventListener('click', function(){
	stopAllAudio();
	audioOne.play();
})
document.querySelector('#play-2').addEventListener('click', function(){
	stopAllAudio();
	audioTwo.play();
})