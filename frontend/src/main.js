// main.js - Main entry point for the ModularGrid Price Monitor frontend

// Create the Vue app
const app = Vue.createApp({
  data() {
    return {
      isLoggedIn: false,
      username: '',
      deals: [],
      watchlist: [],
      loading: false,
      error: null,
      activeTab: 'dashboard'
    }
  },
  methods: {
    async login(username, password) {
      this.loading = true;
      try {
        // In a real app, this would make an API call to the backend
        console.log('Logging in with:', username);
        // Simulate successful login
        this.isLoggedIn = true;
        this.username = username;
        this.loading = false;
      } catch (error) {
        this.error = 'Login failed. Please check your credentials.';
        this.loading = false;
      }
    },
    logout() {
      this.isLoggedIn = false;
      this.username = '';
    },
    setActiveTab(tab) {
      this.activeTab = tab;
    }
  },
  template: `
    <div class="container mt-4">
      <header class="mb-4">
        <h1 class="text-center">ModularGrid Price Monitor</h1>
      </header>
      
      <div v-if="!isLoggedIn" class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">Login</div>
            <div class="card-body">
              <form @submit.prevent="login(document.getElementById('username').value, document.getElementById('password').value)">
                <div class="mb-3">
                  <label for="username" class="form-label">Username</label>
                  <input type="text" class="form-control" id="username" required>
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" class="form-control" id="password" required>
                </div>
                <button type="submit" class="btn btn-primary" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  Login
                </button>
                <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
              </form>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else>
        <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
          <div class="container-fluid">
            <span class="navbar-brand">Welcome, {{ username }}</span>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
              <ul class="navbar-nav">
                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'dashboard' }" href="#" @click="setActiveTab('dashboard')">Dashboard</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'deals' }" href="#" @click="setActiveTab('deals')">Deals</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'watchlist' }" href="#" @click="setActiveTab('watchlist')">Watchlist</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'settings' }" href="#" @click="setActiveTab('settings')">Settings</a>
                </li>
              </ul>
              <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                  <a class="nav-link" href="#" @click="logout">Logout</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        
        <div v-if="activeTab === 'dashboard'" class="row">
          <div class="col-md-12">
            <div class="card">
              <div class="card-header">Dashboard</div>
              <div class="card-body">
                <p>Welcome to the ModularGrid Price Monitor. This tool helps you track eurorack module prices on ModularGrid marketplace.</p>
                <div class="alert alert-info">
                  <i class="fas fa-info-circle"></i> This is a simplified version of the application for demonstration purposes.
                </div>
                <button class="btn btn-primary">Start Monitoring</button>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="activeTab === 'deals'" class="row">
          <div class="col-md-12">
            <div class="card">
              <div class="card-header">Deals</div>
              <div class="card-body">
                <p>No deals found yet. Start monitoring to find good deals on eurorack modules.</p>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="activeTab === 'watchlist'" class="row">
          <div class="col-md-12">
            <div class="card">
              <div class="card-header">Watchlist</div>
              <div class="card-body">
                <p>Your watchlist is empty. Add modules to your watchlist to track their prices.</p>
                <div class="input-group mb-3">
                  <input type="text" class="form-control" placeholder="Module name">
                  <button class="btn btn-outline-secondary" type="button">Add to Watchlist</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="activeTab === 'settings'" class="row">
          <div class="col-md-12">
            <div class="card">
              <div class="card-header">Settings</div>
              <div class="card-body">
                <h5>ModularGrid Account</h5>
                <div class="mb-3">
                  <label for="mg-username" class="form-label">ModularGrid Username</label>
                  <input type="text" class="form-control" id="mg-username">
                </div>
                <div class="mb-3">
                  <label for="mg-password" class="form-label">ModularGrid Password</label>
                  <input type="password" class="form-control" id="mg-password">
                </div>
                <button class="btn btn-primary">Save Settings</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
});

// Mount the app
app.mount('#app');
