const API_URL = 'http://127.0.0.1:8000/api/members/';
let currentPage = 1;

document.addEventListener('DOMContentLoaded', () => {
    fetchMembers();

    // Form submission
    document.getElementById('memberForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const memberData = {
            name: document.getElementById('name').value,
            sex: document.getElementById('sex').value,
            age: parseInt(document.getElementById('age').value) || 18,
            address: document.getElementById('address').value || 'الارض',
            phone_number: document.getElementById('phone_number').value,
            telegram_id: document.getElementById('telegram_id').value,
            email: document.getElementById('email').value,
            telgram_username: document.getElementById('telgram_username').value,
            colleage: document.getElementById('colleage').value,
            working_untill: document.getElementById('working_untill').value
        };

        await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(memberData)
        });
        fetchMembers();
        e.target.reset();
    });

    // Pagination and Filtering
    document.getElementById('prevPage').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            fetchMembers();
        }
    });
    document.getElementById('nextPage').addEventListener('click', () => {
        currentPage++;
        fetchMembers();
    });
    document.getElementById('search').addEventListener('input', fetchMembers);
    document.getElementById('sexFilter').addEventListener('change', fetchMembers);
});

async function fetchMembers() {
    const search = document.getElementById('search').value;
    const sex = document.getElementById('sexFilter').value;
    let url = `${API_URL}?page=${currentPage}`;
    if (search) url += `&search=${search}`;
    if (sex) url += `&sex=${sex}`;

    const response = await fetch(url);
    const data = await response.json();

    const tbody = document.getElementById('membersTable');
    tbody.innerHTML = '';
    data.results.forEach(member => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="p-2">${member.name}</td>
            <td class="p-2">${member.sex === 'M' ? 'ذكر' : 'انثى'}</td>
            <td class="p-2">${member.age}</td>
            <td class="p-2">${member.phone_number}</td>
            <td class="p-2">${member.email}</td>
            <td class="p-2">
                <button onclick="deleteMember(${member.id})" class="bg-red-500 text-white p-1 rounded hover:bg-red-600">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    // Pagination controls
    document.getElementById('prevPage').disabled = !data.previous;
    document.getElementById('nextPage').disabled = !data.next;
    document.getElementById('pageInfo').textContent = `Page ${currentPage} of ${Math.ceil(data.count / 10)}`;
}

async function deleteMember(id) {
    if (confirm('Are you sure you want to delete this member?')) {
        await fetch(`${API_URL}${id}/`, { method: 'DELETE' });
        fetchMembers();
    }
}
