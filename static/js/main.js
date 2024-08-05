document.addEventListener('DOMContentLoaded', function () {
    const root = document.documentElement;
    const navMenuButton = document.getElementById("nav-menu-icon");
    const navMenuIcons = navMenuButton.querySelectorAll('hr');
    const navMenu = document.getElementById("nav-menu");

    navMenuButton.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        let isActive = navMenu.classList.contains('active');
        navMenu.style.height = isActive ? navMenu.scrollHeight + "px" : "0px";
        navMenuIcons.forEach((hr, key) => hr.classList.toggle(`rotated-hr${key + 1}`));
    });


    const toggleButton = document.getElementById('theme-toggle');
    const toggleButtonIcon = toggleButton.querySelector('i');
    toggleButton.addEventListener('click', () => {
        const currentTheme = root.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        toggleButtonIcon.classList.toggle('fa-moon');
        toggleButtonIcon.classList.toggle('fa-circle-half-stroke');
    });

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        root.setAttribute('data-theme', savedTheme);
        toggleButtonIcon.classList.toggle('fa-moon');
        toggleButtonIcon.classList.toggle('fa-circle-half-stroke');
    }


    const conversionRates = {
        ethToUsd: 3497.43
    };

    // fetch('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
    //     .then(res => res.json())
    //     .then(data => conversionRates.ethToUsd = data.ethereum.usd)
    //     .catch(error => console.error("cannot fetch eth to usd api" + error));

    function convertEthToUsd(ethAmount) {
        return ethAmount * conversionRates.ethToUsd;
    }

    function truncateText(text, length) {
        return text.length > length ? text.slice(0, length) + '...' : text;
    }

    function formatDateToISOString(date) {
        return date.toISOString().split('T')[0];
    }

    document.querySelectorAll('.auto-scroll').forEach((scrollbar, key) => {
        let maxScrollWidth = scrollbar.scrollWidth - scrollbar.clientWidth;
        scrollbar.scrollLeft = key % 2 == 0 ? 0 : maxScrollWidth;
        let direction = 1;
        let pause = false;

        setInterval(() => {
            if (!pause) {
                scrollbar.scrollBy(direction, 0);

                if (scrollbar.scrollLeft >= maxScrollWidth) {
                    direction = -1;
                    pause = true;
                    setTimeout(() => { pause = false; }, 1000);
                }
                else if (scrollbar.scrollLeft <= 0) {
                    direction = 1;
                    pause = true;
                    setTimeout(() => { pause = false; }, 1000);
                }
            }
        }, 30)
    });

    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const dropdownContent = dropdown.querySelector('.dropdown-content');
        const dropdownButton = dropdown.querySelector('.dropdown-btn');
        const dropdownIcon = dropdownButton.querySelector('.arrow-icon');

        let toggle = !dropdownContent.classList.contains('opened');
        dropdownIcon.style.transform = `rotate(${toggle ? 0 : 180}deg)`;
        dropdownContent.style.height = toggle ? "0px" : dropdownContent.scrollHeight + "px";

        dropdownButton.addEventListener('click', () => {
            toggle = dropdownContent.style.height !== "0px";
            dropdownIcon.style.transform = `rotate(${toggle ? 0 : 180}deg)`;
            dropdownContent.style.height = toggle ? "0px" : dropdownContent.scrollHeight + "px";
        });
    });

    document.querySelectorAll('.show-more').forEach(moreButton => {
        const textElement = moreButton.parentElement.querySelector('.extra-content');
        const fullText = textElement.innerHTML;
        const length = +textElement.getAttribute('data-length');
        textElement.innerHTML = truncateText(fullText, length);
        let isTruncated = true;

        moreButton.addEventListener('click', () => {
            if (isTruncated) {
                textElement.innerHTML = fullText;
                moreButton.textContent = 'Show less';
            }
            else {
                textElement.innerHTML = truncateText(fullText, length);
                moreButton.textContent = 'Show more';
            }

            isTruncated = !isTruncated;
        });
    });

    document.querySelectorAll('.like-btn').forEach(likeBtn => {
        likeBtn.addEventListener('click', () => {
            likeBtn.classList.toggle('fa-regular');
            likeBtn.classList.toggle('fa-solid');
        })
    });

    document.querySelectorAll('.popup-close-btn').forEach(popupCloseBtn => {
        popupCloseBtn.addEventListener('click', () => {
            popupCloseBtn.closest('.popup-section').classList.remove('active');
        });
    });

    document.querySelectorAll('.eth').forEach(eth => {
        const usd = eth.parentElement.querySelector('.usd');
        const usdAmount = convertEthToUsd(parseFloat(eth.textContent));
        usd.textContent = `$${usdAmount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    });

    const termCheckbox = document.querySelector('.term-check-icon');
    if (termCheckbox) {
        const termCheckIcon = termCheckbox.querySelector('.check-icon');

        termCheckbox.addEventListener('click', () => {
            termCheckIcon.classList.toggle('hidden');
            let isChecked = !termCheckIcon.classList.contains('hidden');

            document.querySelectorAll('.auction-button').forEach(auctionBtn => {
                auctionBtn.disabled = !isChecked;
            });
        });
    }

    if (document.getElementById('nft-create-form')) {
        const imageInput = document.getElementById('upload-image-input');
        imageInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const imgElement = document.getElementById('uploaded-image');
                    imgElement.src = e.target.result;
                    imgElement.classList.remove('hidden');
                    document.getElementById('no-new-image').classList.add('hidden');
                };
                reader.readAsDataURL(file);
            }
        });
    }

    if (document.getElementById('nft-sell-form')) {
        const priceInput = document.getElementById('price-input');
        const priceDisplay = document.getElementById('price-display');
        const currencySelect = document.getElementById('currency');
        const popupEndTime = document.getElementById('popup-end-time');
        const popupPrice = document.getElementById('popup-price');
        const startTimeInput = document.getElementById('start-time');
        const endTimeInput = document.getElementById('end-time');
        const scheduleSelect = document.getElementById('schedule-time');

        const today = formatDateToISOString(new Date());
        startTimeInput.setAttribute('min', today);
        startTimeInput.value = today;

        updateEndTime();
        scheduleSelect.addEventListener('change', updateEndTime);
        startTimeInput.addEventListener('change', updateEndTime);

        function updateEndTime() {
            const scheduleValue = scheduleSelect.value.split('-');
            const startDate = new Date(startTimeInput.value);
            let endDate = new Date(startDate);

            if (scheduleValue[1] === 'month') {
                endDate.setMonth(endDate.getMonth() + +scheduleValue[0]);
            }
            else if (scheduleValue[1] === 'year') {
                endDate.setFullYear(endDate.getFullYear() + +scheduleValue[0]);
            }

            endTimeInput.value = formatDateToISOString(endDate);
            endTimeInput.setAttribute('min', startTimeInput.value);
        }


        priceInput.addEventListener('input', () => {
            const currency = currencySelect.value;
            const price = +parseFloat(priceInput.value).toFixed(2) || 0;
            priceDisplay.textContent = `${price} ${currency}`;
        });

        document.getElementById('complete-listing-btn').addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('listing-popup').classList.add('active');
            popupEndTime.textContent = endTimeInput.value;
            popupPrice.textContent = priceDisplay.textContent;
        });

        document.getElementById('sign-btn').addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('completed-popup').classList.add('active');
        });
    }

    if (document.getElementById('register-form')) {
        const loginBtn = document.getElementById('login-btn');
        const registerBtn = document.getElementById('register-btn');
        const loginPopup = document.getElementById('login-popup');
        const isLoginActive = localStorage.getItem('isLoginActive');

        if (isLoginActive === 'true') {
            loginPopup.classList.add('active');
        }

        loginBtn.addEventListener('click', () => {
            loginPopup.classList.add('active');
            localStorage.setItem('isLoginActive', 'true');
        });

        registerBtn.addEventListener('click', () => {
            loginPopup.classList.remove('active');
            localStorage.setItem('isLoginActive', 'false');
        });


        const avatars = document.querySelectorAll('#avatar-selection .avatar-img');
        const previewAvatar = document.querySelector('#avatar-preview .avatar-img');
        const avatarInput = document.querySelector('#avatar-input');
        previewAvatar.src = avatars[0].src;
        avatarInput.value = avatars[0].getAttribute('data-avatar-id');

        avatars.forEach(avatar => {
            avatar.addEventListener('click', () => {
                const src = avatar.src;
                const id = avatar.getAttribute('data-avatar-id');
                previewAvatar.src = src;
                avatarInput.value = id;
            });
        });


        const fullNameInput = document.getElementById('fullNameInput');
        const previewFullname = document.getElementById('previewFullname');

        fullNameInput.addEventListener('input', () => {
            const fullName = fullNameInput.value;
            previewFullname.textContent = fullName;
        });


        document.querySelectorAll('.password-show-btn').forEach(passwordShowBtn => {
            const passwordInput = passwordShowBtn.parentElement.querySelector('input');

            passwordShowBtn.addEventListener('click', () => {
                passwordShowBtn.classList.toggle('fa-eye-slash');
                passwordShowBtn.classList.toggle('fa-eye');
                passwordInput.type = passwordInput.type === 'text' ? 'password' : 'text';
            });
        });
    }

    if (document.querySelector('.connect-wallet-section')) {
        const walletPopup = document.querySelector('.popup-section');
        const walletCancelBtn = document.getElementById('wallet-cancel-btn');

        walletCancelBtn.addEventListener('click', (e) => {
            e.preventDefault();
            walletPopup.classList.remove('active');
        });

        document.querySelectorAll('.wallet').forEach(wallet => {
            wallet.addEventListener('click', () => {
                walletPopup.classList.add('active');
                const walletImage = wallet.querySelector('.wallet-image img');
                const walletName = wallet.querySelector('.wallet-name');
                const walletType = document.querySelector('input[name="connect-wallet"]:checked + label');
                walletPopup.querySelector('.wallet-image img').src = walletImage.src;
                walletPopup.querySelector('.wallet-name').textContent = walletName.textContent;
                walletPopup.querySelector('.wallet-info').textContent = walletType.textContent;
            })
        })
    }


    const collectionSection = document.querySelector('.collection-section');
    if (collectionSection) {
        const collectionFilters = collectionSection.querySelector('.collection-cards-filters');
        const nftTimes = collectionSection.querySelectorAll('.nft-time');
        const searchRemoveBtn = collectionSection.querySelector('.remove-search-btn');
        const nftSearchInput = collectionSection.querySelector('#nft-search');
        const collectionSearchInput = collectionSection.querySelector('#collection-search');


        if (nftSearchInput) {
            const nftCardsParent = collectionSection.querySelector('.collection-nft-cards');
            const nftCards = nftCardsParent.querySelectorAll('.nft-card');
            const statusFilters = collectionFilters.querySelectorAll('input[name="status"]');
            const currencyFilters = collectionFilters.querySelectorAll('input[name="currency"]');
            const minValueFilter = document.getElementById('min-value');
            const maxValueFilter = document.getElementById('max-value');
            statusFilters.forEach(cb => cb.addEventListener('change', FilterNfts));
            currencyFilters.forEach(rb => rb.addEventListener('change', FilterNfts));
            nftSearchInput.addEventListener('input', FilterNfts);
            searchRemoveBtn.addEventListener('click', () => {
                nftSearchInput.value = '';
                nftSearchInput.focus();
                FilterNfts();
            });
            minValueFilter.addEventListener('input', FilterNfts);
            maxValueFilter.addEventListener('input', FilterNfts);

            const sortByFilter = document.getElementById('sort-by');
            sortByFilter.addEventListener('change', FilterNfts);

            function FilterNfts() {
                const selectedStatusFilters = Array.from(statusFilters).filter(cb => cb.checked).map(cb => cb.value);
                const selectedCurrency = collectionSection.querySelector('input[name="currency"]:checked').value;
                const searchText = nftSearchInput.value.toLowerCase();
                const minValue = parseFloat(minValueFilter.value);
                const maxValue = parseFloat(maxValueFilter.value);
                const sortBy = sortByFilter.value;
                searchRemoveBtn.classList.toggle('hidden', !searchText);

                const filteredCards = Array.from(nftCards).filter(card => {
                    const cardStatus = card.getAttribute('data-status');
                    const cardCurrency = card.getAttribute('data-currency');
                    const cardContent = card.textContent.toLowerCase();
                    const cardPrice = parseFloat(card.getAttribute('data-price'));

                    const matchesStatus = !selectedStatusFilters.length || selectedStatusFilters.includes(cardStatus);
                    const matchesCurrency = selectedCurrency === 'all' || cardCurrency === selectedCurrency;
                    const matchesSearchText = cardContent.includes(searchText);
                    const matchesMinValue = isNaN(minValue) || cardPrice >= minValue;
                    const matchesMaxValue = isNaN(maxValue) || cardPrice <= maxValue;

                    return matchesStatus && matchesCurrency && matchesSearchText && (matchesMinValue && matchesMaxValue);
                });

                const sortedCards = filteredCards.sort((a, b) => {
                    const priceA = parseFloat(a.getAttribute('data-price'));
                    const priceB = parseFloat(b.getAttribute('data-price'));
                    const nameA = a.textContent.toLowerCase();
                    const nameB = b.textContent.toLowerCase();

                    switch (sortBy) {
                        case 'price-asc':
                            return priceA - priceB;
                        case 'price-desc':
                            return priceB - priceA;
                        case 'name-asc':
                            return nameA.localeCompare(nameB);
                        case 'name-desc':
                            return nameB.localeCompare(nameA);
                        default:
                            return 0;
                    }
                });

                nftCardsParent.innerHTML = '';
                sortedCards.forEach(card => nftCardsParent.appendChild(card));
            }


        }

        if (collectionSearchInput) {
            const collectionCardsParent = collectionSection.querySelector('.collection-cards');
            const collectionCards = Array.from(collectionCardsParent.querySelectorAll('.collection-card'));
            const categoryFilters = collectionFilters.querySelectorAll('input[name="category"]');
            const blockchainFilter = collectionSection.querySelector('#blockchains');
            const sortByFilter = document.getElementById('sort-by-collection');

            categoryFilters.forEach(cb => cb.addEventListener('change', FilterCollections));
            blockchainFilter.addEventListener('change', FilterCollections);
            collectionSearchInput.addEventListener('input', FilterCollections);
            sortByFilter.addEventListener('change', FilterCollections);
            searchRemoveBtn.addEventListener('click', () => {
                collectionSearchInput.value = '';
                collectionSearchInput.focus();
                FilterCollections();
            });

            function FilterCollections() {
                const selectedCategories = Array.from(categoryFilters).filter(cb => cb.checked).map(cb => cb.value);
                const selectedBlockchain = blockchainFilter.value;
                const searchText = collectionSearchInput.value.toLowerCase();
                const sortBy = sortByFilter.value;
                searchRemoveBtn.classList.toggle('hidden', !searchText);

                const filteredCards = collectionCards.filter(card => {
                    const cardCategory = card.getAttribute('data-category');
                    const cardBlockchain = card.getAttribute('data-blockchain');
                    const cardContent = card.textContent.toLowerCase();

                    const matchesCategory = selectedCategories.length === 0 || selectedCategories.includes(cardCategory);
                    const matchesBlockchain = selectedBlockchain === 'all' || cardBlockchain === selectedBlockchain;
                    const matchesSearchText = cardContent.includes(searchText);

                    return matchesCategory && matchesBlockchain && matchesSearchText;
                });

                const sortedCards = filteredCards.sort((a, b) => {
                    const nameA = a.textContent.toLowerCase();
                    const nameB = b.textContent.toLowerCase();

                    switch (sortBy) {
                        case 'name-asc':
                            return nameA.localeCompare(nameB);
                        case 'name-desc':
                            return nameB.localeCompare(nameA);
                        default:
                            return 0;
                    }
                });

                collectionCardsParent.innerHTML = '';
                sortedCards.forEach(card => collectionCardsParent.appendChild(card));
            }
        }



        if (collectionFilters) {
            const switch1 = document.getElementById('switch1');
            const switch2 = document.getElementById('switch2');
            const switch3 = document.getElementById('switch3');


            if (switch1) {
                switch1.addEventListener('change', function () {
                    if (switch1.checked) {
                        // root.style.setProperty('--nft-cards-count', 3);
                        collectionFilters.classList.remove('layout-3');
                    }
                });
            }

            if (switch2) {
                switch2.addEventListener('change', function () {
                    if (switch2.checked) {
                        // root.style.setProperty('--collection-cards-count', 3);
                        // root.style.setProperty('--nft-cards-count', 4);
                        collectionFilters.classList.remove('layout-3');
                    }
                });
            }

            if (switch3) {
                switch3.addEventListener('change', function () {
                    if (switch3.checked) {
                        // root.style.setProperty('--collection-cards-count', 4);
                        // root.style.setProperty('--nft-cards-count', 4);
                        collectionFilters.classList.add('layout-3');
                    }
                });
            }
        }

        nftTimes.forEach(nftTime => {
            const nftTimeText = nftTime.querySelector('span');
            const dateString = nftTimeText.textContent.trim();
            const datePattern = /(\w+)\.?\ (\d+), (\d+), (\d+):(\d+) (a\.m\.|p\.m\.)/;
            const match = dateString.match(datePattern);

            if (match) {
                const monthMap = {
                    'Jan': 0, 'Feb': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5,
                    'July': 6, 'Aug': 7, 'Sept': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
                };

                const month = monthMap[match[1]];
                const day = parseInt(match[2], 10);
                const year = parseInt(match[3], 10);
                let hour = parseInt(match[4], 10);
                const minute = parseInt(match[5], 10);
                const period = match[6];

                if (period === 'p.m.' && hour !== 12) {
                    hour += 12;
                } else if (period === 'a.m.' && hour === 12) {
                    hour = 0;
                }

                const nftEndTime = new Date(Date.UTC(year, month, day, hour, minute));

                if (!isNaN(nftEndTime)) {
                    const today = new Date();
                    const isToday = (
                        year === today.getFullYear() &&
                        month === today.getMonth() &&
                        day === today.getDate()
                    );

                    if (nftEndTime < today) {
                        nftTimeText.textContent = 'Expired';
                        nftTime.classList.add('expired');
                    }
                    else if (isToday) {
                        nftTimeText.textContent = nftEndTime.toLocaleTimeString();
                    }
                    else {
                        nftTimeText.textContent = formatDateToISOString(nftEndTime);
                    }
                } else {
                    console.error(`Invalid date: ${nftTimeText.textContent}`);
                }
            } else {
                console.error(`Invalid date format: ${nftTimeText.textContent}`);
            }
        });


    }
});
