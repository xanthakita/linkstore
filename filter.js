document.addEventListener('DOMContentLoaded', function() {
    const tagFilters = document.getElementById('tagFilters');
    const sections = document.getElementById('sections');
    let activeFilters = {};

    // Generate radio buttons for filtering by category
    function generateTagFilters() {
        const allTags = new Set();
        for (const section of sections.children) {
            const tags = section.querySelectorAll('span[id]');
            tags.forEach(tag => allTags.add(tag.id));
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
    }

    // Update active filters when checkbox state changes

    // Update active filters when checkbox state changes
    function updateFilters(event) {
        const checkbox = event.target;
        console.log("Clicked checkbox value:", checkbox.value);
        if (checkbox.checked) {
            activeFilters[checkbox.value] = true;
        } else {
            delete activeFilters[checkbox.value];
        }
        filterEntries();
    }

    // Filter entries based on active filters
    function filterEntries() {
        for (const section of sections.children) {
            const tags = section.querySelectorAll('span[id]');
            let showSection = true;
            tags.forEach(tag => {
                if (!(tag.id in activeFilters)) {
                    showSection = false;
                }
            });
            if (showSection) {
                section.classList.remove('hidden');
            } else {
                section.classList.add('hidden');
            }
        }
    }

    // Initial setup
    generateTagFilters();

    // Add event listener to generateTagFilters
    document.addEventListener('change', generateTagFilters);

    // Add event listener to updateFilters
    document.addEventListener('change', updateFilters);
});

