
// load the youtube api
const tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
document.head.appendChild(tag);

const videoList = document.getElementById("video-list");
const videoModal = document.getElementById("video-modal");
const previousButton = document.getElementById("previous-video-button");
const nextButton = document.getElementById("next-video-button");
const youtubeVideos = document.querySelectorAll('div.youtube-card');
let player; // holds the youtube player object

// get all the video id's
const youtubeVideoIds = [];
youtubeVideos.forEach(video => {
    youtubeVideoIds.push(video.dataset.videoId);
});

// find the adjacent entries in an array
const findAdjacentIds = (id, idArray) => {
    const index = idArray.indexOf(id);
    let previousId = '';
    let nextId = '';
    if (index !== -1) {
        if (index > 0) {
            previousId = idArray[index - 1];
        }
        if (index < idArray.length - 1) {
            nextId = idArray[index + 1];
        }
    }
    return {
        previous: previousId,
        next: nextId
    };
}
// load a video (autostart) and set prev/next video id's
const playVideo = (videoID) => {
    player.videoLoaded = false; // used to set position to 0sec
    player.loadVideoById(videoID, startSeconds = 0);
    const adjacents = findAdjacentIds(videoID, youtubeVideoIds);
    previousButton.setAttribute("data-target", adjacents.previous);
    nextButton.setAttribute("data-target", adjacents.next);
}

// close modal - stop video, hide modal
const closeModal = () => {
    player.stopVideo();
    videoModal.classList.remove('show');
}

// event listeners
videoModal.addEventListener("click", function (event) {
    if (event.target === videoModal) {
        closeModal();
    }
});
previousButton.addEventListener("click", function (event) {
    playVideo(previousButton.dataset.target);
});
nextButton.addEventListener("click", function (event) {
    playVideo(nextButton.dataset.target);
});

// called when youtube api completes loading: creates the player iframe
window.onYouTubeIframeAPIReady = () => {
    player = new YT.Player('card-video-iframe', {
        playerVars: {
            'playsinline': 1
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

// called when player iframe complates loading
// - add video list click listener
// - remove 'loading' class disable spinners and change cursor to pointer 
const onPlayerReady = (event) => {
    videoList.addEventListener("click", function (event) {
        let targetElement = event.target;
        while (targetElement !== null) {
            if (targetElement.classList.contains("youtube-card")) {
                playVideo(targetElement.dataset.videoId);
                videoModal.classList.add('show');
                return;
            }
            targetElement = targetElement.parentElement;
        }
    });
    videoList.classList.remove('loading');
}

// fixes bug where api ignores start position and will play video from last user's last played position instead
// set videoLoaded=true as player constantly changes state between PLAYING and BUFFERING
const onPlayerStateChange = (event) => {
    if (event.data == YT.PlayerState.PLAYING && !player.videoLoaded) {
        player.pauseVideo();
        player.seekTo(0);
        player.playVideo();
        player.videoLoaded = true;
    }
}