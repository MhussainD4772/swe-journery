const API_BASE = "http://localhost:8000";
export const TOKEN_KEY = "access_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

export async function apiFetch(
  path: string,
  options: RequestInit = {},
): Promise<Response> {
  const token = getToken();
  const headers = new Headers(options.headers);

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  // Login 401 (no token yet) is a normal failed credential check — return it.
  // 401 with a token means the session expired.
  if (response.status === 401 && token) {
    clearToken();
    window.location.assign("/login");
    throw new Error("Unauthorized");
  }

  return response;
}
