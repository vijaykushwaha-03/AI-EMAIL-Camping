const API_BASE_URL = 'http://localhost:8000/api';

// Generic fetch wrapper
async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
        throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
}

// Types
export interface Contact {
    id: string;
    email: string;
    name: string;
    company: string;
    tags: string[];
    is_subscribed: boolean;
    created_at: string;
}

export interface ContactsResponse {
    count: number;
    results: Contact[];
    next: string | null;
    previous: string | null;
}

export interface Campaign {
    id: string;
    name: string;
    subject: string;
    content: string;
    status: 'draft' | 'scheduled' | 'sending' | 'sent';
    sent_count: number;
    open_count: number;
    click_count: number;
    open_rate: number;
    click_rate: number;
    recipient_count: number;
    scheduled_at: string | null;
    created_at: string;
}

export interface DashboardStats {
    stats: {
        total_sent: number;
        total_contacts: number;
        open_rate: number;
        click_rate: number;
        bounce_rate: number;
    };
    chart_data: { date: string; sent: number; opened: number }[];
    recent_campaigns: {
        id: string;
        name: string;
        status: string;
        open_rate: number;
        created_at: string;
    }[];
}

export interface GeneratedEmail {
    subject: string;
    title: string;
    body: string;
    cta_text: string;
}

// API Functions

// Contacts
export const getContacts = (page = 1, search = '') =>
    apiRequest<ContactsResponse>(`/contacts/?page=${page}${search ? `&search=${search}` : ''}`);

export const createContact = (data: { email: string; name?: string; company?: string }) =>
    apiRequest<Contact>('/contacts/', {
        method: 'POST',
        body: JSON.stringify(data),
    });

export const deleteContact = (id: string) =>
    apiRequest(`/contacts/${id}/`, { method: 'DELETE' });

export const importContacts = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/contacts/import_csv/`, {
        method: 'POST',
        body: formData,
    });
    return response.json();
};

// Campaigns
export const getCampaigns = async (): Promise<Campaign[]> => {
    const response = await apiRequest<{ results: Campaign[] } | Campaign[]>('/campaigns/');
    // Handle both paginated and non-paginated responses
    if (Array.isArray(response)) {
        return response;
    }
    return response.results || [];
};

export const getCampaign = (id: string) =>
    apiRequest<Campaign>(`/campaigns/${id}/`);

export const createCampaign = (data: { name: string; subject: string; content?: string }) =>
    apiRequest<Campaign>('/campaigns/', {
        method: 'POST',
        body: JSON.stringify(data),
    });

export const updateCampaign = (id: string, data: Partial<Campaign>) =>
    apiRequest<Campaign>(`/campaigns/${id}/`, {
        method: 'PUT',
        body: JSON.stringify(data),
    });

export const deleteCampaign = (id: string) =>
    apiRequest(`/campaigns/${id}/`, { method: 'DELETE' });

export const sendCampaign = (id: string, testMode = false) =>
    apiRequest<{ sent: number; failed: number; message: string }>(`/campaigns/${id}/send/`, {
        method: 'POST',
        body: JSON.stringify({ test_mode: testMode }),
    });

// Analytics
export const getDashboardStats = () =>
    apiRequest<DashboardStats>('/analytics/dashboard/');

// AI
export const generateEmail = (prompt: string, provider = 'OpenRouter') =>
    apiRequest<GeneratedEmail>('/ai/generate/', {
        method: 'POST',
        body: JSON.stringify({ prompt, provider }),
    });
