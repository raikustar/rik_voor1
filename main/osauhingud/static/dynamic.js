
document.addEventListener("DOMContentLoaded", function() {
    let add_individual_entity_button = document.getElementById("add_individual_entity_button");
    let add_legal_entity_button = document.getElementById("add_legal_entity_button");
    let grandParentLeft = document.querySelector(".shareholders_box_left");
    let grandParentRight = document.querySelector(".shareholders_box_right");

    const dynamic_entity_buttons_left = document.querySelector(".dynamic_entity_buttons_left");
    let debl_bool = false
    const dynamic_entity_buttons_right = document.querySelector(".dynamic_entity_buttons_right");
    let debr_bool = false


    function createRemoveEntityButton(parent_element, button_text, button_class) {
        const btn = document.createElement("button");
        btn.textContent = button_text;
        btn.className = button_class
        parent_element.appendChild(btn);
    }



    function createIndividualEntity() {
        
        const parent = document.createElement("div");
        parent.className = "add_entity_shares";

        const header = document.createElement("h3");
        header.textContent = "Individual Shareholder";

        const firstNameInput = document.createElement("input");
        firstNameInput.type = "text";
        firstNameInput.name = "individual_first_name[]";
        firstNameInput.placeholder = "First Name";

        const lastNameInput = document.createElement("input");
        lastNameInput.type = "text";
        lastNameInput.name = "individual_last_name[]";
        lastNameInput.placeholder = "Last Name";

        const personalIdInput = document.createElement("input");
        personalIdInput.type = "text";
        personalIdInput.name = "individual_personal_id[]";
        personalIdInput.placeholder = "Personal ID Code";

        const shareInput = document.createElement("input");
        shareInput.type = "number";
        shareInput.name = "individual_share[]";
        shareInput.placeholder = "Share";

        parent.appendChild(header);
        parent.appendChild(firstNameInput);
        parent.appendChild(lastNameInput);
        parent.appendChild(personalIdInput);
        parent.appendChild(shareInput);

        grandParentLeft.appendChild(parent);

        if (grandParentLeft.childElementCount > 0 && debl_bool == false) {
            createRemoveEntityButton(dynamic_entity_buttons_left, "Remove Entity Field", "ind_ent_btn")
            debl_bool = true
            removeEntityButtonFunction("ind_ent_btn", grandParentLeft)
        } 
    }

    
    function createLegalEntity() {
        const parent = document.createElement("div");
        parent.className = "add_entity_shares";

        const header = document.createElement("h3");
        header.textContent = "Legal Entity Shareholder";

        const legalEntityName = document.createElement("input");
        legalEntityName.type = "text";
        legalEntityName.name = "legal_entity_name[]";
        legalEntityName.placeholder = "Entity Name";

        const legalEntityRegistryCode = document.createElement("input");
        legalEntityRegistryCode.type = "text";
        legalEntityRegistryCode.name = "legal_entity_registry_code[]";
        legalEntityRegistryCode.placeholder = "Registry Code";

        const legalEntityShare = document.createElement("input");
        legalEntityShare.type = "number";
        legalEntityShare.name = "legal_entity_share[]";
        legalEntityShare.placeholder = "Share";

        const br = document.createElement("br");

        parent.appendChild(header)
        parent.appendChild(legalEntityName)
        parent.appendChild(legalEntityRegistryCode)
        parent.appendChild(legalEntityShare)
        parent.appendChild(br)

        grandParentRight.appendChild(parent);

        if (grandParentRight.childElementCount > 0 && debr_bool == false) {
            createRemoveEntityButton(dynamic_entity_buttons_right, "Remove Legal Field", "leg_ent_btn")
            debr_bool = true
            removeEntityButtonFunction("leg_ent_btn", grandParentRight)
        } 
    }

    function removeEntityButtonFunction(class_name, grnd_parent) {
        // individual entity button
        let btn = document.querySelector("." + class_name)
        if (btn) {
            console.log("Button pressed")
            btn.addEventListener("click", function() {
                if (grnd_parent && grnd_parent.lastElementChild){
                    grnd_parent.removeChild(grnd_parent.lastElementChild)
                }
            })
            
        }
    }




    add_individual_entity_button.addEventListener("click", createIndividualEntity);
    add_legal_entity_button.addEventListener("click", createLegalEntity);

    
});