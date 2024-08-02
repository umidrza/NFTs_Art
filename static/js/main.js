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


    let ethToUsdRate = 3497.43;
    fetch('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
        .then(res => res.json())
        .then(data => ethToUsdRate = data.ethereum.usd)
        .catch(error => console.error("cannot fetch eth to usd api" + error));

    function convertEthToUsd(ethAmount) {
        return ethAmount * ethToUsdRate;
    }

    function truncateText(text, length) {
        return text.length > length ? text.slice(0, length) + '...' : text;
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
            console.log(dropdownContent.scrollHeight);
        });
    });

    document.querySelectorAll('.show-more').forEach(moreButton => {
        const textElement = moreButton.parentElement.querySelector('.extra-content');
        const fullText = textElement.innerHTML;
        const length = +textElement.getAttribute('data-length');
        textElement.innerHTML = truncateText(fullText, length);

        moreButton.addEventListener('click', () => {
            if (moreButton.textContent == 'Show more') {
                textElement.innerHTML = fullText;
                moreButton.textContent = 'Show less';
            }
            else {
                textElement.innerHTML = truncateText(fullText, length);
                moreButton.textContent = 'Show more';
            }
        });
    });

    document.querySelectorAll('.like-btn').forEach(likeBtn => {
        likeBtn.addEventListener('click', () => {
            likeBtn.classList.toggle('fa-regular');
            likeBtn.classList.toggle('fa-solid');
        })
    });

    document.querySelectorAll('.term-check-icon').forEach(checkBox => {
        const checkIcon = checkBox.querySelector('.check-icon');

        checkBox.addEventListener('click', () => {
            checkIcon.classList.toggle('hidden');
            let isChecked = !checkIcon.classList.contains('hidden');

            document.querySelectorAll('.auction-button').forEach(auctionBtn => {
                auctionBtn.disabled = !isChecked;
            });
        });
    });

    document.querySelectorAll('.eth').forEach(eth => {
        const usd = eth.parentElement.querySelector('.usd');
        const usdAmount = convertEthToUsd(parseFloat(eth.textContent));
        usd.textContent = `$${usdAmount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    });

    document.querySelectorAll('.popup-close-btn').forEach(popupCloseBtn => {
        popupCloseBtn.addEventListener('click', () => {
            popupCloseBtn.closest('.popup-section').classList.remove('active');
        });
    });



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
        const currencySelect = document.getElementById('currency');
        const priceDisplay = document.getElementById('price-display');
        const scheduleSelect = document.getElementById('schedule-time');
        const startTimeInput = document.getElementById('start-time');
        const endTimeInput = document.getElementById('end-time');
        const popupEndTime = document.getElementById('popup-end-time');
        const popupPrice = document.getElementById('popup-price');

        const today = new Date().toISOString().split('T')[0];
        startTimeInput.setAttribute('min', today);
        startTimeInput.value = today;
        updateEndTime();

        priceInput.addEventListener('input', function () {
            const currency = currencySelect.value;
            const price = parseFloat(priceInput.value).toFixed(2) || 0;
            priceDisplay.textContent = `${price} ${currency}`;
        });

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

            endTimeInput.value = endDate.toISOString().split('T')[0];
        }

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


    const collectionFilters = document.querySelector('.collection-cards-filters');
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


        document.querySelectorAll('.remove-search-btn').forEach(removeSearchBtn => {
            const input = removeSearchBtn.parentElement.querySelector('input');

            removeSearchBtn.addEventListener('click', () => {
                input.value = '';
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
});
