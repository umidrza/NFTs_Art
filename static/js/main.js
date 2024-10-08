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
        ethToUsd: 2637.50
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

        if (length >= fullText.length){
            moreButton.classList.add('hidden');
            return;
        }

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

    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.classList.add('deactive');
        }, 3000); 
    
        setTimeout(() => {
            alert.remove();
        }, 3500);
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

    document.querySelectorAll('.difference').forEach(diffElement => {
        const nftPrice = parseFloat(diffElement.getAttribute('data-price'));
        const bidAmount = parseFloat(diffElement.getAttribute('data-bid-amount'));
        const quantity = parseFloat(diffElement.getAttribute('data-quantity'));
        const percentage = (((bidAmount - nftPrice * quantity) / nftPrice) * 100).toFixed(0);

        if(nftPrice && bidAmount && quantity){
            if (percentage > 0) {
                diffElement.textContent = `${percentage}% above`;
            } else {
                diffElement.textContent = `${Math.abs(percentage)}% below`;
            }
        }
        else{
            diffElement.textContent = 'N/A'
        }
    });

    document.querySelectorAll('.countdown').forEach(countdownElement => {
        const endTime = new Date(countdownElement.getAttribute('data-date')).getTime();
        const now = new Date().getTime();
        const timeDifference = endTime - now;

        if (timeDifference > 0) {
            const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
            const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));

            if (countdownElement.classList.contains('days')){
                countdownString = `${days} days`;
            }
            else{
                countdownString = `${days.toString().padStart(2, '0')}d : ${hours.toString().padStart(2, '0')}h : ${minutes.toString().padStart(2, '0')}m`;
            }
            countdownElement.textContent = countdownString;
            
        } else {
            countdownElement.textContent = 'Expired';
            countdownElement.classList.add('expired');
        }
    })

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
        const startTimeInput = document.getElementById('start-time');
        const endTimeInput = document.getElementById('end-time');
        const scheduleSelect = document.getElementById('schedule-time');

        const today = formatDateToISOString(new Date());
        startTimeInput.setAttribute('min', today);
        startTimeInput.value = today;

        updatePrice();
        updateEndTime();
        scheduleSelect.addEventListener('change', updateEndTime);
        startTimeInput.addEventListener('change', updateEndTime);
        priceInput.addEventListener('input', updatePrice);

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

        function updatePrice() {
            const selectedCurrency = currencySelect.options[currencySelect.selectedIndex];
            const currency = selectedCurrency.textContent;
            const price = +parseFloat(priceInput.value).toFixed(2) || 0;
            priceDisplay.textContent = `${price} ${currency}`;
        }

        const walletLink = document.querySelector('.popup-nft-link');
        if(walletLink){
            const walletKey = walletLink.querySelector('.popup-wallet-link');
            const copyBtn = walletLink.querySelector('.wallet-copy-btn');
            const fullKey = walletKey.getAttribute('data-key');
            const truncatedKey = `0x${fullKey.slice(0, 7)}...K${fullKey.slice(-3)}`;
            walletKey.textContent = truncatedKey;

            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(fullKey);
                copyBtn.classList.toggle('fa-solid');
                copyBtn.classList.toggle('fa-regular');
            });
        }
    }

    if (document.getElementById('register-form')) {
        const loginBtn = document.getElementById('login-btn');
        const registerBtn = document.getElementById('register-btn');
        const loginPopup = document.getElementById('login-popup');
        const isLoginActive = localStorage.getItem('isLoginActive');

        if (isLoginActive === 'true' && loginPopup) {
            loginPopup.classList.add('active');
        }

        if (loginBtn){
            loginBtn.addEventListener('click', () => {
                
                loginPopup.classList.add('active');
                localStorage.setItem('isLoginActive', 'true');
            });
        }

        if (registerBtn){
            registerBtn.addEventListener('click', () => {
                loginPopup.classList.remove('active');
                localStorage.setItem('isLoginActive', 'false');
            });
        }

        
        const avatars = document.querySelectorAll('#avatar-selection .avatar-img');
        const previewAvatar = document.querySelector('#avatar-preview .avatar-img');
        const avatarInput = document.querySelector('#avatar-input');

        let selectedAvatar = [...avatars].find(avatar => avatar.getAttribute('data-avatar-id') === avatarInput.value);

        if (selectedAvatar) {
            previewAvatar.src = selectedAvatar.src;
            avatarInput.value = selectedAvatar.getAttribute('data-avatar-id');
        }
        else {
            previewAvatar.src = avatars[0].src;
            avatarInput.value = avatars[0].getAttribute('data-avatar-id');
        }

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

        if (fullNameInput.value){
            previewFullname.textContent = fullNameInput.value;
        }

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
                passwordInput.focus();
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
                wallet.querySelector('input[name="provider"]').checked = true;
                const walletImage = wallet.querySelector('.wallet-image img');
                const walletName = wallet.querySelector('.wallet-name');
                const walletBlockchain = document.querySelector('input[name="blockchain"]:checked + label');
                walletPopup.querySelector('.wallet-image img').src = walletImage.src;
                walletPopup.querySelector('.wallet-name').textContent = walletName.textContent;
                walletPopup.querySelector('.wallet-info').textContent = walletBlockchain.textContent;
            });
        });
    }

    if (document.querySelector('.collection-section')) {
        const collectionFilters = document.querySelector('.collection-cards-filters');

        const switch1 = document.getElementById('switch1');
        const switch2 = document.getElementById('switch2');
        const switch3 = document.getElementById('switch3');
        let pageWidth = window.innerWidth;
        
        function updateCardCounts(cardsCount, collectionCount) {
            root.style.setProperty('--nft-cards-count', cardsCount);
            root.style.setProperty('--collection-cards-count', collectionCount);
        }
        
        function handleSwitchChange() {
            pageWidth = window.innerWidth;
            if (switch1 && switch1.checked) {
                if (pageWidth > 1200) { 
                    updateCardCounts(3, 3);
                } else if (pageWidth > 992) { 
                    updateCardCounts(2, 2);
                }
                collectionFilters.classList.remove('layout-2');
                collectionFilters.classList.remove('layout-3');
            } else if (switch2 && switch2.checked) {
                if (pageWidth > 1200) { 
                    updateCardCounts(4, 3);
                } else if (pageWidth > 992) {
                    updateCardCounts(3, 2);
                }
                collectionFilters.classList.add('layout-2');
                collectionFilters.classList.remove('layout-3');
            } else if (switch3 && switch3.checked) {
                if (pageWidth > 1200) { 
                    updateCardCounts(4, 4);
                } else if (pageWidth > 992) {
                    updateCardCounts(3, 3);
                }
                collectionFilters.classList.remove('layout-2');
                collectionFilters.classList.add('layout-3');
            }
        }
        
        if (switch1) {
            switch1.addEventListener('change', handleSwitchChange);
            if(pageWidth < 992) {
                switch1.parentElement.classList.add('hidden');
            }
        }
        
        if (switch2) {
            switch2.addEventListener('change', handleSwitchChange);
        }
        
        if (switch3) {;
            switch3.addEventListener('change', handleSwitchChange);
            if (pageWidth < 992) {
                switch3.checked = true;
            }
        }

        handleSwitchChange();
    }
});
