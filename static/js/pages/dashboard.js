// Dashboard page logic: list, search, edit, delete patients
(function(){
  function renderTable(tbody, data) {
    tbody.innerHTML = '';
    data.forEach(patient => {
      const row = document.createElement('tr');
      row.setAttribute('data-id', patient.id);
      row.innerHTML = `
        <td><img class="patient-photo" src="/static/uploads/${patient.photoFilename || 'default.jpg'}" alt="Photo"></td>
        <td>${patient.name || ''}</td>
        <td>${patient.age || ''}</td>
        <td>${patient.gender || ''}</td>
        <td>${patient.contact || ''}</td>
        <td>${patient.address || ''}</td>
        <td>${patient.chiefComplaint || ''}</td>
        <td>${patient.painLevel || ''}</td>
        <td>${patient.painDescription || ''}</td>
        <td>${patient.additionalSymptoms || ''}</td>
        <td>${patient.medicalHistory || ''}</td>
        <td>${patient.emergencyName || ''}</td>
        <td>${patient.emergencyRelation || ''}</td>
        <td>${patient.emergencyGender || ''}</td>
        <td>${patient.emergencyContact || ''}</td>
        <td>${patient.emergencyAddress || ''}</td>
        <td>${patient.heart_rate || ''}</td>
        <td>${patient.spo2 || ''}</td>
        <td>${patient.body_temperature || ''}</td>
        <td>${patient.environment_temperature || ''}</td>
        <td>
          <button class="view">View</button>
          <button class="edit">Edit</button>
          <button class="delete">Delete</button>
        </td>`;
      tbody.appendChild(row);
    });
  }

  function attachRowHandlers(tbody) {
    tbody.addEventListener('click', (e) => {
      const btn = e.target.closest('button');
      if (!btn) return;
      const row = btn.closest('tr');
      const id = row?.getAttribute('data-id');
      if (!id) return;

      if (btn.classList.contains('view')) {
        window.location.href = `patient-details.html?id=${id}`;
      } else if (btn.classList.contains('edit')) {
        const cells = row.querySelectorAll('td');
        for (let i = 1; i <= 15; i++) {
          if (cells[i]) {
            const val = cells[i].innerText;
            cells[i].innerHTML = `<input type="text" value="${val}" style="width:100%;">`;
          }
        }
        if (cells[20]) {
          cells[20].innerHTML = `
            <button class="save">Save</button>
            <button class="cancel">Cancel</button>`;
        }
      } else if (btn.classList.contains('delete')) {
        if (!confirm('Are you sure you want to delete this patient?')) return;
        fetch(`/delete_patient/${id}`, { method: 'DELETE' })
          .then(res => { if (!res.ok) throw new Error('Failed to delete'); return res.json(); })
          .then(out => { if (out.status === 'success') { alert('Patient deleted'); loadPatients(); } else { alert('Error: ' + out.message); } })
          .catch(() => alert('Failed to delete patient.'));
      } else if (btn.classList.contains('save')) {
        const inputs = row.querySelectorAll('input');
        if (inputs.length < 15) { alert('Error: Not all fields found for editing.'); return; }
        const ageValue = parseInt(inputs[1].value);
        const painLevelValue = parseInt(inputs[6].value);
        if (isNaN(ageValue)) { alert('Please enter a valid number for age.'); return; }
        if (isNaN(painLevelValue)) { alert('Please enter a valid number for pain level.'); return; }
        const updatedData = {
          name: inputs[0].value,
          age: ageValue,
          gender: inputs[2].value,
          contact: inputs[3].value,
          address: inputs[4].value,
          chiefComplaint: inputs[5].value,
          painLevel: painLevelValue,
          painDescription: inputs[7].value,
          additionalSymptoms: inputs[8].value,
          medicalHistory: inputs[9].value,
          emergencyName: inputs[10].value,
          emergencyRelation: inputs[11].value,
          emergencyGender: inputs[12].value,
          emergencyContact: inputs[13].value,
          emergencyAddress: inputs[14].value
        };
        fetch(`/update_patient/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(updatedData) })
          .then(res => { if (!res.ok) throw new Error('Update failed'); return res.json(); })
          .then(out => { if (out.status === 'success') { alert('Patient updated successfully'); loadPatients(); } else { alert('Error: ' + out.message); } })
          .catch(() => alert('Update failed.'));
      } else if (btn.classList.contains('cancel')) {
        loadPatients();
      }
    });
  }

  let patientsData = [];

  function loadPatients() {
    const tbody = document.querySelector('#patientTable tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    fetch('/patients')
      .then(res => { if (!res.ok) throw new Error('Network response was not OK'); return res.json(); })
      .then(data => { patientsData = data; renderTable(tbody, data); })
      .catch(() => { tbody.innerHTML = '<tr><td colspan="21">Error loading data</td></tr>'; });
  }

  function attachSearch() {
    const searchInput = document.getElementById('searchInput');
    const tbody = document.querySelector('#patientTable tbody');
    if (!searchInput || !tbody) return;
    searchInput.addEventListener('input', () => {
      const filter = searchInput.value.toLowerCase();
      const filtered = patientsData.filter(patient =>
        (patient.name && patient.name.toLowerCase().includes(filter)) ||
        (patient.age && String(patient.age).includes(filter)) ||
        (patient.chiefComplaint && patient.chiefComplaint.toLowerCase().includes(filter))
      );
      renderTable(tbody, filtered);
    });
  }

  function attachExport() {
    window.exportCSV = function(){
      fetch('/export_csv')
        .then(r => { if (!r.ok) throw new Error('Failed to export CSV'); return r.blob(); })
        .then(blob => { const url = window.URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = 'patients.csv'; document.body.appendChild(a); a.click(); document.body.removeChild(a); window.URL.revokeObjectURL(url); })
        .catch(() => alert('Export failed.'));
    };
  }

  window.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('patientTable')) return;
    loadPatients();
    attachSearch();
    attachRowHandlers(document.querySelector('#patientTable tbody'));
    attachExport();
  });
})();



