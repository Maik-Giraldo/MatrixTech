export interface verifyTokenResponse {
    verified: boolean,
    data: Data,
    message: string
}

interface Data {
    name: string,
    last_name: string,
    email: string,
    phone_number: string,
    city: string,
    country: string,
    img_profile: string,
}