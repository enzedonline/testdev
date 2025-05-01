class VideoList {
    constructor() {
        this.videoListContainer = document.getElementById("video-list-container");
        this.videoList = this.videoListContainer.querySelector("div#video-list");
        this.videoListPaginator = document.getElementById("video-list-paginator");
        this.videoCards = Array.from(this.videoListContainer.querySelectorAll("div.youtube-card"));
        this.videoModal = this.videoListContainer.querySelector("div#video-modal");
        this.previousVideoButton = this.videoListContainer.querySelector("div#video-modal-previous");
        this.nextVideoButton = this.videoListContainer.querySelector("div#video-modal-next");
        this.videoModalDismiss = this.videoListContainer.querySelector("button#video-modal-dismiss");
        this.pagination = JSON.parse(this.videoListContainer.querySelector("script#pagination").textContent);
        this.videoListContainer.dataset.cardsLoading = false;
        this.videoLoaded = false;

        this.loadYoutubeAPI();
        this.createCardTemplate();
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
        // preload additional videos if pagination enabled and near end of loaded playlist
        const videoCard = this.videoList.querySelector(`div#${cardId}`)
        if (videoCard) {
            let index = this.videoCards.indexOf(videoCard);
            // previous/next are empty if first/last card (empty data-target buttons hidden via css)
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

    createCardTemplate() {
        // Create a DocumentFragment to hold the card structure
        this.cardTemplate = document.createDocumentFragment();

        // Create the card container
        const card = document.createElement('div');
        card.classList.add('card', 'youtube-card');

        // Add video div with image and SVG
        const videoDiv = document.createElement('div');
        videoDiv.classList.add('card-video');
        const img = document.createElement('img');
        img.classList.add('card-video-thumbnail');
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.classList.add('youtube-logo');
        const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
        use.setAttribute('href', '#icon-youtube-logo');
        svg.appendChild(use);
        videoDiv.append(img, svg);
        card.appendChild(videoDiv);

        // Add card body with title, author, and description
        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');
        const title = document.createElement('p');
        title.classList.add('h5', 'card-title');
        const author = document.createElement('p');
        author.classList.add('h6', 'card-text', 'card-author');
        const description = document.createElement('div');
        description.classList.add('card-description');
        cardBody.append(title, author, description);
        card.appendChild(cardBody);

        // Add card footer with date
        const cardFooter = document.createElement('div');
        cardFooter.classList.add('card-footer');
        const updatedText = document.createElement('p');
        updatedText.classList.add('h6', 'card-updated');
        updatedText.textContent = 'Updated ';
        const date = document.createElement('span');
        date.classList.add('card-date');
        updatedText.appendChild(date);
        cardFooter.appendChild(updatedText);
        card.appendChild(cardFooter);

        // Append the card structure to the DocumentFragment
        this.cardTemplate.appendChild(card);
    }

    async loadCards(auto = true) {
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
                    // increment current_page and fetch data for next page from api
                    const url = `${window.location.href}api/page/${++this.pagination.current_page}/`;
                    const response = await fetch(url);
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    const result = await response.json();
                    const videoData = result.videos;
                    this.pagination = result.pagination;
                    // create cards for each video
                    videoData.forEach(video => {
                        this.addVideoCard(video);
                    })
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

    addVideoCard(video) {
        const cardClone = this.cardTemplate.cloneNode(true);
        const card = cardClone.querySelector('.card')
        card.id = video.card_id;
        card.dataset.videoId = video.video_id;
        cardClone.querySelector('.card-video-thumbnail').src = video.thumbnail_url;
        cardClone.querySelector('.card-title').textContent = video.title;
        cardClone.querySelector('.card-author').textContent = video.author_name;
        cardClone.querySelector('.card-description').textContent = video.description;
        cardClone.querySelector('.card-date').textContent = this.localiseDate(video.last_updated);
        this.videoList.appendChild(cardClone);
    }

    closeModal = () => {
        // close modal - stop video, hide modal
        window.player.stopVideo();
        this.videoModal.classList.remove('show');
    }

    paginatorObserver = new IntersectionObserver((entries, observer) => {
        // watch for video-list-paginator div entering viewport
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (this.pagination.enabled) {
                    this.triggerEndlessScroll();
                } else {
                    this.paginatorObserver.unobserve(entry.target);
                }
            }
        });
    }, {
        root: null, // Use the viewport as the root
        rootMargin: '0px 0px 150px 0px', // Trigger when 150px or less from the bottom
        threshold: 0 // Trigger as soon as it enters the rootMargin area
    });

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
        // watch for video-list-paginator div entering viewport if paginating
        if (this.pagination.enabled) {
            this.paginatorObserver.observe(this.videoListPaginator);
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
