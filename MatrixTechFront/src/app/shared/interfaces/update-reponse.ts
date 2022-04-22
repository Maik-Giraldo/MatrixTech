export interface updateResponse {
    updated: boolean,
    message: string,
    data?: Data
}

interface Data {
    name: string,
    last_name: string,
    email: string,
    img_profile: string,
    password: string,
    phone_number: string,
    city: string,
    country: string
}