class VideoList {
    constructor() {
        window.test = this
        this.videoListContainer = document.getElementById("video-list-container");
        this.videoList = this.videoListContainer.querySelector("div#video-list");
        this.videoCards = Array.from(this.videoListContainer.querySelectorAll("div.youtube-card"));
        this.videoModal = this.videoListContainer.querySelector("div#video-modal");
        this.previousVideoButton = this.videoListContainer.querySelector("div#video-modal-previous");
        this.nextVideoButton = this.videoListContainer.querySelector("div#video-modal-next");
        this.videoModalDismiss = this.videoListContainer.querySelector("button#video-modal-dismiss");
        this.pagination = JSON.parse(this.videoListContainer.querySelector("script#pagination").textContent);
        this.videoListContainer.dataset.cardsLoading = false;
        this.videoLoaded = false;
        this.loadYoutubeAPI();
        this.addEventListeners();
        if (this.pagination.enabled) {
            this.loadCards();
        }
    }

    loadYoutubeAPI() {
        // load the youtube api
        const tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        document.head.appendChild(tag);
        // called when youtube api completes loading: creates the player iframe
        // onYouTubeIframeAPIReady must be created in window context
        window.onYouTubeIframeAPIReady = () => {
            window.player = new YT.Player('card-video-iframe', {
                playerVars: {
                    'playsinline': 1
                },
                events: {
                    'onReady': this.onPlayerReady,
                    'onStateChange': this.onPlayerStateChange
                }
            });
        }
    }

    onPlayerReady = (event) => {
        // called when player iframe completes loading - changes card behaviour
        // via css: hides spinner, shows youtube logo, changes pointer to cursor
        // via js: enables click
        this.videoListContainer.dataset.playerLoading = false;
    }

    onPlayerStateChange = (event) => {
        if (!this.videoLoaded) {
            // bug fix: playVideoById() (and cueVideoById()) can ignore startSeconds attribute 
            //   if user has part watched this video before, video will resume from where the user last left of instead
            //   force video to start at 0 seconds by pausing video, using seekTo then restarting video
            //   player muted during initial buffering to prevent audio fragment before video set to 0 seconds
            //   use this.videoLoaded boolean flag to ensure only run once
            if (event.data == YT.PlayerState.PLAYING) {
                this.videoLoaded = true;
                window.player.pauseVideo();
                window.player.seekTo(0);
                window.player.unMute()
                window.player.playVideo();
            }
            else if (event.data == YT.PlayerState.BUFFERING) {
                window.player.mute();
            }
        } else if (event.data == YT.PlayerState.ENDED && this.nextVideoButton.dataset.target) {
            // autoplay next video when finished if not last video
            const nextVideo = this.nextVideoButton.dataset.target
            this.playVideo(nextVideo);
        }
    }

    playVideo = (cardId) => {
        // load a video (autostart) and set prev/next video id's
        const videoId = this.videoList.querySelector(`div#${cardId}`).dataset.videoId
        this.videoLoaded = false;
        window.player.loadVideoById({ 'videoId': videoId, 'startSeconds': 0 });
        this.setAdjacentIds(cardId);
    }

    async setAdjacentIds(cardId) {
        // get id's for adjacent cards and load into prev/next buttons data-target
        // use card id's, not video id's - video id's may not be unique
        // the next button attribute used also for autoplaying next video on end
        // preload additional videos if pagination enabled and near end of playlist
        const videoCard = this.videoList.querySelector(`div#${cardId}`)
        if (videoCard) {
            let index = this.videoCards.indexOf(videoCard);
            // previous/next are emtpy if first/last card (empty data-target buttons hidden via css)
            let previous = index > 0 ? this.videoCards[index - 1].id : '';
            let next = index < this.videoCards.length - 1 ? this.videoCards[index + 1].id : '';
            this.previousVideoButton.setAttribute("data-target", previous);
            this.nextVideoButton.setAttribute("data-target", next);
            // preload additional videos if last or 2nd last video in playlist
            if (this.pagination.enabled && (index > this.videoCards.length - 3)) {
                await this.loadCards(false);
                if (next === '') {
                    index = this.videoCards.indexOf(videoCard);
                    next = index < this.videoCards.length - 1 ? this.videoCards[index + 1].id : '';
                    this.nextVideoButton.setAttribute("data-target", next);
                }
            }
        }
    }

    async loadCards(auto=true) {
        // if auto===true load, next set of videos only if bottom of videlist less than 150px below bottom of screen
        // only run if not all pages have loaded
        if (this.pagination.enabled) {
            const containerRect = this.videoList.getBoundingClientRect();
            const viewportHeight = window.innerHeight;
            const containerBottom = containerRect.bottom;
            if (!auto || containerBottom <= viewportHeight + 150) {
                // fetch next page of video card data and update card set
                try {
                    // triggers fade in/out effect on thumbnail via css
                    this.videoListContainer.dataset.cardsLoading = true;
                    // fetch data for next page from api
                    const url = `${window.location.href}api/page/${++this.pagination.current_page}/`;
                    const response = await fetch(url);
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    const result = await response.json();
                    this.videoData = result.videos;
                    this.pagination = result.pagination;
                    // create additional cards for loaded videos
                    let loadedCards = ""
                    for (let i = 0; i < this.videoData.length; i++) {
                        loadedCards += this.cardHTMLFragment(
                            this.videoData[i].card_id,
                            this.videoData[i].video_id,
                            this.videoData[i].thumbnail_url,
                            this.videoData[i].title,
                            this.videoData[i].author_name,
                            this.videoData[i].description,
                            this.localiseDate(this.videoData[i].last_updated)
                        )
                    }
                    this.videoList.insertAdjacentHTML('beforeend', loadedCards);
                    // load more cards if base of video list still within 150px of screen bottom
                    await this.loadCards();
                    // refresh playlist
                    this.videoCards = Array.from(this.videoListContainer.querySelectorAll("div.youtube-card"));
                    // end fade in/out effect on thumbnail via css - delay by 500ms
                    setTimeout(() => {
                        this.videoListContainer.dataset.cardsLoading = false;
                        // final check if new card set needed - required if scrolled to end of page during loading
                        window.dispatchEvent(new Event('scroll'));
                    }, 500);
                } catch (error) {
                    console.error('There was a problem with the fetch operation:', error);
                    this.videoListContainer.dataset.cardsLoading = false;
                }
            }
        }
    }

    cardHTMLFragment(card_id, video_id, thumbnail_url, title, author_name, description, last_updated) {
        // template for video card
        return `
        <div class="card youtube-card" id="${card_id}" data-video-id="${video_id}">
            <div class="card-video">
                <img class="card-video-thumbnail" src="${thumbnail_url}">
                <svg class="youtube-logo">
                    <use href="#icon-youtube-logo"></use>
                </svg>
            </div>
            <div class="card-body">
                <p class="h5 card-title">${title}</p>
                <p class="h6 card-text card-author">${author_name}</p>
                <div class="card-description">${description}</div>
            </div>
            <div class="card-footer">
                <p class="h6 card-updated">
                    Updated <span class="card-date">${last_updated}</span>
                </p>
            </div>
        </div>
        `
    }

    closeModal = () => {
        // close modal - stop video, hide modal
        window.player.stopVideo();
        this.videoModal.classList.remove('show');
    }

    addEventListeners() {
        // close modal if click anywhere on modal background
        this.videoModal.addEventListener("click", (event) => {
            if (event.target === this.videoModal) {
                this.closeModal();
            }
        });
        // close modal if click on close button
        this.videoModalDismiss.addEventListener("click", (event) => {
            this.closeModal();
        });
        // play previous video when click on modal left arrow
        this.previousVideoButton.addEventListener("click", (event) => {
            this.playVideo(this.previousVideoButton.dataset.target);
        });
        // play next video when click on modal right arrow
        this.nextVideoButton.addEventListener("click", (event) => {
            this.playVideo(this.nextVideoButton.dataset.target);
        });
        // open video when click anywhere on a video card
        this.videoList.addEventListener("click", (event) => {
            let targetElement = event.target;
            while (targetElement !== null) {
                if (targetElement.classList.contains("youtube-card")) {
                    this.playVideo(targetElement.id);
                    this.videoModal.classList.add('show');
                    return;
                }
                targetElement = targetElement.parentElement;
            }
        });
        // watch for scroll events if paginating
        if (this.pagination.enabled) {
            window.addEventListener('scroll', this.triggerEndlessScroll.bind(this), { passive: true });
        }
    }

    triggerEndlessScroll() {
        // pagination.enabled===true until last page loaded - ignore scroll event once fully loaded
        // only trigger loadCards while cards not loading - ignore further scroll events until cards loaded
        if (this.pagination.enabled && this.videoListContainer.dataset.cardsLoading !== 'true') {
            this.loadCards();
        }
    }

    localiseDate(dateTimeString) {
        // display date in local format and adjust for local timezone
        try {
            const date = new Date(dateTimeString);
            const options = {
                day: '2-digit',
                month: 'long',
                year: 'numeric'
            };
            return date.toLocaleDateString(undefined, options);
        } catch (error) {
            console.error(`Could not convert ${dateTimeString} to a date: `, error);
        }
    }

}
