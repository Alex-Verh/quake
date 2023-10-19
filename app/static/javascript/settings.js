document.addEventListener("DOMContentLoaded",  () => {

    const editAddressBtn = document.querySelector("#edit-address-button");
    const enableNotifyBtn = document.querySelector("#enable-notify-button");
    const emailModal = document.querySelector("#email-modal");
    const emailModalClose = emailModal.querySelector(".email-modal__close");
    const emailModalText = emailModal.querySelector(".email-modal__text");

    // Settings Range Sliders //
    document.querySelectorAll(".settings-block__slider").forEach((element, index) => {
        element.addEventListener("input", () => {
            if (index < 2) {
                element.parentElement.previousElementSibling.querySelector("span.bold").innerHTML = element.value + ".0°"; 
            } else if (index < 3){
                element.parentElement.previousElementSibling.querySelector("span.bold").innerHTML = element.value + "%"; 
            } else if (element.value == 0) {
                element.parentElement.previousElementSibling.querySelector("span.bold").innerHTML = "OFF"; 
            } else {
                element.parentElement.previousElementSibling.querySelector("span.bold").innerHTML = "ON"; 
            }
        })
    });

    // Settings Edit Personal //
    editAddressBtn.addEventListener("click", () => {
        const emailInput = editAddressBtn.parentElement.previousElementSibling.querySelector(".settings-block__input");

        if (!emailInput.readOnly) {
            if (validateEmail(emailInput.value).isValid) {
                // !TODO : Fetch changes of new email to the backend
                editAddressBtn.innerHTML = "edit address"
                editAddressBtn.classList.remove("settings-block__button_active");
                emailInput.readOnly = true;
            } else {
                emailModal.classList.remove("none");
                emailModalText.innerHTML = validateEmail(emailInput.value).detail;
            }
        } else {
            emailInput.readOnly = false;
            emailInput.select();
            editAddressBtn.classList.add("settings-block__button_active");
            editAddressBtn.innerHTML = "save email"
        }
    })

    enableNotifyBtn.addEventListener("click", () => {
        enableNotifyBtn.classList.toggle("settings-block__button_active");
        if (enableNotifyBtn.classList.contains("settings-block__button_active")) {
            enableNotifyBtn.innerHTML = "enabled"
        } else {
            enableNotifyBtn.innerHTML = "disabled"
        }
    })

    // Modal Listeners //
    emailModalClose.addEventListener("click", function() {
        emailModal.classList.add("none");
    });

    // Email Validation Function // 
    const validateEmail = (email, options = {}) => {
        const {
            regEx = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i,
        } = options;
        if (!email) {
            return {isValid: false, detail: "Email address is required."};
        }
        if (!regEx.test(email)) {
            return {isValid: false, detail: "Invalid address, enter a valid email."};
        }
        return {isValid: true};
    };
    
});