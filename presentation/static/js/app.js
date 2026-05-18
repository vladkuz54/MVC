// App state
let state = {
    user: null,
    token: null,
    activeTab: 'dashboard'
};

// API base URLs
const API = {
    auth: '/auth',
    organizations: '/organizations',
    devices: '/devices',
    sensors: '/sensors',
    readings: '/readings',
    alerts: '/alerts',
    users: '/users'
};

// Check authentication
function checkAuth() {
    const token = localStorage.getItem('nexus_token');
    const userData = localStorage.getItem('nexus_user');
    
    if (!token) {
        window.location.href = '/login';
        return false;
    }
    
    state.token = token;
    state.user = JSON.parse(userData);
    
    // Update sidebar profile
    document.getElementById('nav-username').textContent = state.user.username;
    document.getElementById('nav-role').textContent = state.user.role || 'user';
    document.getElementById('nav-avatar').textContent = state.user.username.substring(0, 2).toUpperCase();
    
    return true;
}

// Global Headers helper
function getHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${state.token}`
    };
}

// Toast Notifications helper
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icon = type === 'success' ? 
        `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--state-success)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>` :
        `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--state-error)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`;
        
    toast.innerHTML = `
        ${icon}
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = '0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Modal open/close helpers
function openModal(id) {
    document.getElementById(id).style.display = 'flex';
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    if (checkAuth()) {
        setupEventListeners();
        loadTabContent('dashboard');
    }
});

// Event Listeners setup
function setupEventListeners() {
    // Sidebar Tabs
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const tabName = item.getAttribute('data-tab');
            
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            
            loadTabContent(tabName);
        });
    });
    
    // Logout
    document.getElementById('logout-button').addEventListener('click', () => {
        localStorage.removeItem('nexus_token');
        localStorage.removeItem('nexus_user');
        showToast('Logged out successfully');
        setTimeout(() => window.location.href = '/login', 500);
    });
}

// Load Tab Content routing
async function loadTabContent(tabName) {
    state.activeTab = tabName;
    
    // Hide all panels
    const panels = document.querySelectorAll('.tab-panel');
    panels.forEach(panel => panel.classList.remove('active'));
    
    // Show selected panel
    const targetPanel = document.getElementById(`tab-${tabName}`);
    if (targetPanel) targetPanel.classList.add('active');
    
    // Dynamic Action Button header update
    const actionContainer = document.getElementById('tab-actions');
    actionContainer.innerHTML = '';
    
    const pageTitle = document.getElementById('page-title');
    const pageSubtitle = document.getElementById('page-subtitle');
    
    switch (tabName) {
        case 'dashboard':
            pageTitle.textContent = 'Dashboard Overview';
            pageSubtitle.textContent = 'Real-time telemetry and network metrics';
            loadDashboard();
            break;
            
        case 'organizations':
            pageTitle.textContent = 'Organizations Directory';
            pageSubtitle.textContent = 'Manage registered enterprise boundaries';
            actionContainer.innerHTML = `
                <button class="btn btn-primary" onclick="openAddOrgModal()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                    New Organization
                </button>
            `;
            loadOrganizations();
            break;
            
        case 'devices':
            pageTitle.textContent = 'Connected Devices';
            pageSubtitle.textContent = 'View hardware modules and monitor status';
            actionContainer.innerHTML = `
                <button class="btn btn-primary" onclick="openAddDeviceModal()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                    Add Device
                </button>
            `;
            loadDevices();
            break;
            
        case 'sensors':
            pageTitle.textContent = 'Telemetry Sensors';
            pageSubtitle.textContent = 'Calibrate sensor nodes and capture data logs';
            loadSensors();
            break;
            
        case 'alerts':
            pageTitle.textContent = 'System Alerts';
            pageSubtitle.textContent = 'Active system abnormalities and status warnings';
            actionContainer.innerHTML = `
                <button class="btn btn-danger" onclick="openTriggerAlertModal()">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>
                    Simulate Alert
                </button>
            `;
            loadAlerts();
            break;
    }
}

// ---------------------- API LOAD CALLS ----------------------

// Fetch stats and live telemetry for main Dashboard
async function loadDashboard() {
    try {
        const [orgs, devs, sens, alts, rdngs] = await Promise.all([
            fetch(API.organizations, { headers: getHeaders() }).then(r => r.json()),
            fetch(API.devices, { headers: getHeaders() }).then(r => r.json()),
            fetch(API.sensors, { headers: getHeaders() }).then(r => r.json()),
            fetch(API.alerts, { headers: getHeaders() }).then(r => r.json()),
            fetch(API.readings, { headers: getHeaders() }).then(r => r.json())
        ]);
        
        document.getElementById('stat-organizations').textContent = orgs.length;
        document.getElementById('stat-devices').textContent = devs.length;
        document.getElementById('stat-sensors').textContent = sens.length;
        
        // Count unresolved alerts
        const unresolved = alts.filter(a => !a.is_resolved).length;
        document.getElementById('stat-alerts').textContent = unresolved;
        
        // Render 10 latest readings
        const tbody = document.getElementById('dashboard-readings-body');
        tbody.innerHTML = '';
        
        // Sort readings by date descending
        const sortedReadings = rdngs
            .sort((a,b) => new Date(b.timestamp) - new Date(a.timestamp))
            .slice(0, 10);
            
        if (sortedReadings.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: var(--text-secondary);">No telemetry logged yet.</td></tr>`;
            return;
        }
        
        sortedReadings.forEach(r => {
            const sensor = sens.find(s => s.id === r.sensor_id);
            const sType = sensor ? sensor.type : 'Unknown';
            const sUnit = sensor ? sensor.unit : '';
            
            tbody.innerHTML += `
                <tr>
                    <td>#${r.sensor_id}</td>
                    <td><strong style="color: var(--accent-indigo)">${sType}</strong></td>
                    <td>${r.value.toFixed(2)} ${sUnit}</td>
                    <td>${new Date(r.timestamp).toLocaleString()}</td>
                </tr>
            `;
        });
        
    } catch (err) {
        console.error(err);
        showToast('Failed to load Dashboard data', 'error');
    }
}

// Fetch and render Organizations
async function loadOrganizations() {
    try {
        const response = await fetch(API.organizations, { headers: getHeaders() });
        const orgs = await response.json();
        
        const tbody = document.getElementById('organizations-table-body');
        tbody.innerHTML = '';
        
        if (orgs.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-secondary);">No organizations created yet.</td></tr>`;
            return;
        }
        
        orgs.forEach(o => {
            tbody.innerHTML += `
                <tr>
                    <td>#${o.id}</td>
                    <td><strong>${o.name}</strong></td>
                    <td><code style="background-color: var(--bg-tertiary); padding: 4px 8px; border-radius: var(--radius-sm); font-size: 0.85rem;">${o.api_key}</code></td>
                    <td>${new Date(o.created_at).toLocaleDateString()}</td>
                    <td class="actions-column">
                        <button class="btn btn-secondary btn-icon" onclick="openEditOrgModal(${o.id}, '${o.name}', '${o.api_key}')">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 1 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                        </button>
                        <button class="btn btn-danger btn-icon" onclick="deleteOrganization(${o.id})">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                        </button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        console.error(err);
        showToast('Failed to load Organizations', 'error');
    }
}

// Fetch and render Devices
async function loadDevices() {
    try {
        const response = await fetch(API.devices, { headers: getHeaders() });
        const devs = await response.json();
        
        const tbody = document.getElementById('devices-table-body');
        tbody.innerHTML = '';
        
        if (devs.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-secondary);">No devices connected yet.</td></tr>`;
            return;
        }
        
        devs.forEach(d => {
            const statusBadge = d.status ? 
                `<span class="badge badge-active">Online</span>` : 
                `<span class="badge badge-inactive">Offline</span>`;
                
            tbody.innerHTML += `
                <tr>
                    <td>#${d.id}</td>
                    <td><strong style="font-family: monospace;">${d.mac_address}</strong></td>
                    <td>${d.firmware_version}</td>
                    <td>Organization #${d.organization_id}</td>
                    <td>${statusBadge}</td>
                    <td class="actions-column">
                        <button class="btn btn-secondary btn-icon" onclick="openEditDeviceModal(${d.id}, ${d.organization_id}, '${d.mac_address}', '${d.firmware_version}', ${d.status})">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 1 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                        </button>
                        <button class="btn btn-danger btn-icon" onclick="deleteDevice(${d.id})">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                        </button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        console.error(err);
        showToast('Failed to load Devices', 'error');
    }
}

// Fetch and render Sensors and Telemetry readings
async function loadSensors() {
    try {
        const [sens, rdngs] = await Promise.all([
            fetch(API.sensors, { headers: getHeaders() }).then(r => r.json()),
            fetch(API.readings, { headers: getHeaders() }).then(r => r.json())
        ]);
        
        // Render sensors table
        const sensBody = document.getElementById('sensors-table-body');
        sensBody.innerHTML = '';
        if (sens.length === 0) {
            sensBody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-secondary);">No sensors registered.</td></tr>`;
        } else {
            sens.forEach(s => {
                sensBody.innerHTML += `
                    <tr>
                        <td>#${s.id}</td>
                        <td>Device #${s.device_id}</td>
                        <td><strong style="color: var(--accent-indigo)">${s.type}</strong></td>
                        <td>${s.unit}</td>
                        <td class="actions-column">
                            <button class="btn btn-danger btn-icon" onclick="deleteSensor(${s.id})">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                            </button>
                        </td>
                    </tr>
                `;
            });
        }
        
        // Render readings table
        const rdngBody = document.getElementById('readings-table-body');
        rdngBody.innerHTML = '';
        
        // Sort readings by date descending
        const sorted = rdngs.sort((a,b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, 10);
        
        if (sorted.length === 0) {
            rdngBody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-secondary);">No telemetry captured yet.</td></tr>`;
        } else {
            sorted.forEach(r => {
                const sensor = sens.find(s => s.id === r.sensor_id);
                const sType = sensor ? sensor.type : 'Unknown';
                const sUnit = sensor ? sensor.unit : '';
                
                rdngBody.innerHTML += `
                    <tr>
                        <td>#${r.id}</td>
                        <td>Sensor #${r.sensor_id} (${sType})</td>
                        <td><strong>${r.value.toFixed(2)} ${sUnit}</strong></td>
                        <td>${new Date(r.timestamp).toLocaleTimeString()}</td>
                        <td class="actions-column">
                            <button class="btn btn-danger btn-icon" onclick="deleteReading(${r.id})">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                            </button>
                        </td>
                    </tr>
                `;
            });
        }
    } catch (err) {
        console.error(err);
        showToast('Failed to load Sensors & Telemetry', 'error');
    }
}

// Fetch and render Alerts
async function loadAlerts() {
    try {
        const response = await fetch(API.alerts, { headers: getHeaders() });
        const alts = await response.json();
        
        const tbody = document.getElementById('alerts-table-body');
        tbody.innerHTML = '';
        
        if (alts.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-secondary);">No system alerts reported.</td></tr>`;
            return;
        }
        
        alts.forEach(a => {
            const severityClass = `badge-severity-${a.severity.toLowerCase()}`;
            const severityBadge = `<span class="badge ${severityClass}">${a.severity}</span>`;
            
            const resolvedBadge = a.is_resolved ? 
                `<span class="badge badge-active" style="background-color: rgba(16, 185, 129, 0.08);">Resolved</span>` : 
                `<span class="badge badge-inactive">Active</span>`;
                
            const resolveAction = a.is_resolved ? '' : `
                <button class="btn btn-primary btn-icon" onclick="resolveAlert(${a.id}, ${a.device_id}, '${a.severity}', '${a.message.replace(/'/g, "\\'")}')" title="Mark as Resolved">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                </button>
            `;
            
            tbody.innerHTML += `
                <tr>
                    <td>#${a.id}</td>
                    <td>Device #${a.device_id}</td>
                    <td>${severityBadge}</td>
                    <td><strong>${a.message}</strong></td>
                    <td>${resolvedBadge}</td>
                    <td class="actions-column">
                        ${resolveAction}
                        <button class="btn btn-danger btn-icon" onclick="deleteAlert(${a.id})">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                        </button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        console.error(err);
        showToast('Failed to load system Alerts', 'error');
    }
}

// ---------------------- MODAL FORMS OPERATIONS ----------------------

// -- Organizations Modals --
function openAddOrgModal() {
    document.getElementById('org-modal-title').textContent = 'Create Organization';
    document.getElementById('org-id').value = '';
    document.getElementById('org-name').value = '';
    document.getElementById('org-apikey').value = '';
    openModal('org-modal');
}

function openEditOrgModal(id, name, apiKey) {
    document.getElementById('org-modal-title').textContent = 'Edit Organization';
    document.getElementById('org-id').value = id;
    document.getElementById('org-name').value = name;
    document.getElementById('org-apikey').value = apiKey;
    openModal('org-modal');
}

async function handleOrgSubmit(event) {
    event.preventDefault();
    const id = document.getElementById('org-id').value;
    const name = document.getElementById('org-name').value;
    const api_key = document.getElementById('org-apikey').value;
    
    const payload = { name, api_key };
    
    try {
        let response;
        if (id) {
            // Update
            response = await fetch(`${API.organizations}/${id}`, {
                method: 'PUT',
                headers: getHeaders(),
                body: JSON.stringify(payload)
            });
        } else {
            // Create
            response = await fetch(`${API.organizations}/`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify(payload)
            });
        }
        
        if (response.ok) {
            showToast(id ? 'Organization updated' : 'Organization created successfully');
            closeModal('org-modal');
            loadOrganizations();
        } else {
            const err = await response.json();
            showToast(err.detail || 'Error saving organization', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Network error saving organization', 'error');
    }
}

async function deleteOrganization(id) {
    if (!confirm('Are you sure you want to delete this organization? All related devices and users will be removed!')) return;
    
    try {
        const response = await fetch(`${API.organizations}/${id}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        
        if (response.ok) {
            showToast('Organization deleted successfully');
            loadOrganizations();
        } else {
            showToast('Failed to delete organization', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Network error deleting organization', 'error');
    }
}

// -- Devices Modals --
async function openAddDeviceModal() {
    document.getElementById('device-modal-title').textContent = 'Add New Device';
    document.getElementById('device-id').value = '';
    document.getElementById('device-mac').value = '';
    document.getElementById('device-firmware').value = '';
    document.getElementById('device-status').value = 'true';
    
    // Load organizations dropdown
    await populateOrgsDropdown('device-org');
    
    openModal('device-modal');
}

async function openEditDeviceModal(id, orgId, mac, firmware, status) {
    document.getElementById('device-modal-title').textContent = 'Edit Device Configuration';
    document.getElementById('device-id').value = id;
    document.getElementById('device-mac').value = mac;
    document.getElementById('device-firmware').value = firmware;
    document.getElementById('device-status').value = status ? 'true' : 'false';
    
    await populateOrgsDropdown('device-org', orgId);
    
    openModal('device-modal');
}

async function populateOrgsDropdown(elementId, selectedId = null) {
    const response = await fetch(API.organizations, { headers: getHeaders() });
    const orgs = await response.json();
    const dropdown = document.getElementById(elementId);
    dropdown.innerHTML = '';
    
    orgs.forEach(o => {
        const isSelected = o.id === selectedId ? 'selected' : '';
        dropdown.innerHTML += `<option value="${o.id}" ${isSelected}>${o.name} (ID #${o.id})</option>`;
    });
}

async function handleDeviceSubmit(event) {
    event.preventDefault();
    const id = document.getElementById('device-id').value;
    const organization_id = parseInt(document.getElementById('device-org').value);
    const mac_address = document.getElementById('device-mac').value;
    const firmware_version = document.getElementById('device-firmware').value;
    const status = document.getElementById('device-status').value === 'true';
    
    const payload = { organization_id, mac_address, status, firmware_version };
    
    try {
        let response;
        if (id) {
            response = await fetch(`${API.devices}/${id}`, {
                method: 'PUT',
                headers: getHeaders(),
                body: JSON.stringify(payload)
            });
        } else {
            response = await fetch(`${API.devices}/`, {
                method: 'POST',
                headers: getHeaders(),
                body: JSON.stringify(payload)
            });
        }
        
        if (response.ok) {
            showToast(id ? 'Device config updated' : 'Device registered successfully');
            closeModal('device-modal');
            loadDevices();
        } else {
            const err = await response.json();
            showToast(err.detail || 'Error saving device', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Network error saving device', 'error');
    }
}

async function deleteDevice(id) {
    if (!confirm('Are you sure you want to remove this hardware device?')) return;
    try {
        const response = await fetch(`${API.devices}/${id}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        if (response.ok) {
            showToast('Device removed successfully');
            loadDevices();
        } else {
            showToast('Failed to delete device', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Network error deleting device', 'error');
    }
}

// -- Sensors Modals --
async function openAddSensorModal() {
    document.getElementById('sensor-id').value = '';
    document.getElementById('sensor-type').value = '';
    document.getElementById('sensor-unit').value = '';
    
    // Populate devices dropdown
    const devResponse = await fetch(API.devices, { headers: getHeaders() });
    const devs = await devResponse.json();
    const select = document.getElementById('sensor-device');
    select.innerHTML = '';
    devs.forEach(d => {
        select.innerHTML += `<option value="${d.id}">Device #${d.id} (${d.mac_address})</option>`;
    });
    
    openModal('sensor-modal');
}

async function handleSensorSubmit(event) {
    event.preventDefault();
    const device_id = parseInt(document.getElementById('sensor-device').value);
    const type = document.getElementById('sensor-type').value;
    const unit = document.getElementById('sensor-unit').value;
    
    const payload = { device_id, type, unit };
    
    try {
        const response = await fetch(`${API.sensors}/`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(payload)
        });
        if (response.ok) {
            showToast('Sensor interface registered');
            closeModal('sensor-modal');
            loadSensors();
        } else {
            showToast('Failed to save sensor', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Network error saving sensor', 'error');
    }
}

async function deleteSensor(id) {
    if (!confirm('Confirm deletion of this sensor interface?')) return;
    try {
        const response = await fetch(`${API.sensors}/${id}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        if (response.ok) {
            showToast('Sensor removed');
            loadSensors();
        } else {
            showToast('Failed to delete sensor', 'error');
        }
    } catch (err) {
        console.error(err);
    }
}

// -- Readings Modals --
async function openAddReadingModal() {
    // Populate sensors select
    const sensRes = await fetch(API.sensors, { headers: getHeaders() });
    const sens = await sensRes.json();
    const select = document.getElementById('reading-sensor');
    select.innerHTML = '';
    sens.forEach(s => {
        select.innerHTML += `<option value="${s.id}">Sensor #${s.id} (${s.type} in ${s.unit})</option>`;
    });
    document.getElementById('reading-value').value = '';
    openModal('reading-modal');
}

async function handleReadingSubmit(event) {
    event.preventDefault();
    const sensor_id = parseInt(document.getElementById('reading-sensor').value);
    const value = parseFloat(document.getElementById('reading-value').value);
    
    const payload = { sensor_id, value };
    
    try {
        const response = await fetch(`${API.readings}/`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(payload)
        });
        if (response.ok) {
            showToast('Telemetry data logged');
            closeModal('reading-modal');
            loadSensors();
        } else {
            showToast('Failed to save telemetry', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Network error saving telemetry', 'error');
    }
}

async function deleteReading(id) {
    if (!confirm('Delete this reading log?')) return;
    try {
        await fetch(`${API.readings}/${id}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        showToast('Reading log deleted');
        loadSensors();
    } catch (err) {
        console.error(err);
    }
}

// -- Alerts Modals --
async function openTriggerAlertModal() {
    // Populate devices select
    const devResponse = await fetch(API.devices, { headers: getHeaders() });
    const devs = await devResponse.json();
    const select = document.getElementById('alert-device');
    select.innerHTML = '';
    devs.forEach(d => {
        select.innerHTML += `<option value="${d.id}">Device #${d.id} (${d.mac_address})</option>`;
    });
    
    document.getElementById('alert-message').value = '';
    document.getElementById('alert-severity').value = 'Warning';
    document.getElementById('alert-resolved').value = 'false';
    openModal('alert-modal');
}

async function handleAlertSubmit(event) {
    event.preventDefault();
    const device_id = parseInt(document.getElementById('alert-device').value);
    const severity = document.getElementById('alert-severity').value;
    const message = document.getElementById('alert-message').value;
    const is_resolved = document.getElementById('alert-resolved').value === 'true';
    
    const payload = { device_id, severity, message, is_resolved };
    
    try {
        const response = await fetch(`${API.alerts}/`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(payload)
        });
        if (response.ok) {
            showToast('Alert condition simulated successfully');
            closeModal('alert-modal');
            loadAlerts();
        } else {
            showToast('Failed to simulate alert condition', 'error');
        }
    } catch (err) {
        console.error(err);
    }
}

async function resolveAlert(id, deviceId, severity, message) {
    const payload = {
        device_id: deviceId,
        severity: severity,
        message: message,
        is_resolved: true
    };
    
    try {
        const response = await fetch(`${API.alerts}/${id}`, {
            method: 'PUT',
            headers: getHeaders(),
            body: JSON.stringify(payload)
        });
        if (response.ok) {
            showToast('Alert resolved');
            loadAlerts();
        } else {
            showToast('Failed to resolve alert', 'error');
        }
    } catch (err) {
        console.error(err);
    }
}

async function deleteAlert(id) {
    if (!confirm('Confirm deletion of alert warning?')) return;
    try {
        await fetch(`${API.alerts}/${id}`, {
            method: 'DELETE',
            headers: getHeaders()
        });
        showToast('Alert entry deleted');
        loadAlerts();
    } catch (err) {
        console.error(err);
    }
}
