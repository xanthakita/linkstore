document.addEventListener('DOMContentLoaded', function() {
    console.log("Document loaded");
    const tagFilters = document.getElementById('tagFilters');
    console.log("Tag filters element:", tagFilters);
    const sections = document.getElementById('sections');
    console.log("Sections element:", sections);
    let activeFilters = {};

    // Generate radio buttons for filtering by category
    function generateTagFilters() {
        console.log("Generating tag filters...");
        const allTags = new Set();
        for (const section of sections.children) {
            console.log("Processing section:", section);
            const tags = section.classList;
            console.log("Section tags:", tags);
            tags.forEach(tag => allTags.add(tag));
        }

        tagFilters.innerHTML = '';
        allTags.forEach(tag => {
            const label = document.createElement('label');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = tag;
            checkbox.checked = true;
            checkbox.addEventListener('change', updateFilters);
            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(tag));
            tagFilters.appendChild(label);
            tagFilters.appendChild(document.createElement('br'));
        });
        console.log("Tag filters generated successfully.");
    }

    // Update active filters when checkbox state changes
    function updateFilters(event) {
        console.log("Updating filters...");
        const checkbox = event.target;
        if (checkbox.checked) {
            activeFilters[checkbox.value] = true;
        } else {
            delete activeFilters[checkbox.value];
        }
        filterEntries();
    }

    // Filter entries based on active filters
    function filterEntries() {
        console.log("Filtering entries...");
        for (const section of sections.children) {
            const tags = section.classList;
            let showSection = true;
            tags.forEach(tag => {
                if (!(tag in activeFilters)) {
                    showSection = false;
                }
            });
            if (showSection) {
                section.classList.remove('hidden');
            } else {
                section.classList.add('hidden');
            }
        }
        console.log("Entries filtered successfully.");
    }

    // Initial setup
    generateTagFilters();

    // Add event listener to generateTagFilters
    document.addEventListener('change', generateTagFilters);

    // Add event listener to generateTagFilters
    document.addEventListener('change', updateFilters);
});

