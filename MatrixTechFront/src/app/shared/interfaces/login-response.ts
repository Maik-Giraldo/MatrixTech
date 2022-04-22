export interface LoginResponse {
    token?: string;
    data?: Data,
    logged: boolean,
    message: string
}

interface Data {
    id: number,
    name: string,
    last_name: string,
    email: string,
    img_profile: string,
    phone_number: string,
    city: string,
    country: string
}
