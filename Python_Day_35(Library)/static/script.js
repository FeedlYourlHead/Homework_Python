document.addEventListener('DOMContentLoaded', ()=>{
    const searchInput = document.getElementById('search-input');
    const genreFilter = document.getElementById('genre-filter');
    const bookItems = document.querySelectorAll('.book-item');

    function filterBook(){
        const searchText = searchInput ? searchInput.value.toLowerCase() : 'all';
        const selectGenre = genreFilter ? genreFilter.value : 'all';

        bookItems.forEach(item => {
            const title = item.querySelector('.book-title').textContent.toLowerCase();
            const genreData = item.getAttribute('data-genres');

            const titleMatch = title.includes(searchText);

            const genreMatch = selectGenre === 'all' || genreData.includes(selectGenre);

            if (titleMatch && genreMatch){
                item.style.display = '';
            }
            else{
                item.style.display = 'none';
            }
        });
    }
    if (searchInput){
        searchInput.addEventListener('input', filterBook);
        console.log(searchInput.value);
    }
    if (genreFilter){
        genreFilter.addEventListener('change', filterBook);
        console.log(genreFilter.value);
    }
});