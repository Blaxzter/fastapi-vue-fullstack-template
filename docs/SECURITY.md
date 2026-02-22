# Security Policy

Security is very important for this project. 🔒

Learn more about it below. 👇

## Authentication & Security Architecture

This project uses **Auth0** as the primary authentication provider, which provides enterprise-grade security features including:

-   **OAuth 2.0 and OpenID Connect** compliance
-   **Multi-factor authentication (MFA)** support
-   **Social login integrations** (Google, GitHub, etc.)
-   **JWT token management** with automatic rotation
-   **Rate limiting** and bot protection
-   **Secure password policies** and breach detection

### How Security Works

1. **Frontend Authentication**: The Vue.js frontend handles user authentication through Auth0's Universal Login
2. **API Protection**: The FastAPI backend validates JWT tokens from Auth0 on protected endpoints
3. **Token Validation**: All API requests include verification of token signature, expiration, and audience
4. **Role-Based Access Control**: User permissions are managed through Auth0 roles and claims
5. **Secure Communication**: All communication uses HTTPS in production environments

## Versions

The latest version or release is supported.

You are encouraged to write tests for your application and update your versions frequently after ensuring that your tests are passing. This way you will benefit from the latest features, bug fixes, and **security fixes**.

## Reporting a Vulnerability

If you think you found a vulnerability, and even if you are not sure about it, please report it right away by creating a security issue at: https://github.com/Blaxzter/fastapi-vue-fullstack-template/issues

Please try to be as explicit as possible, describing all the steps and example code to reproduce the security issue. When creating the issue, please label it with "security" and mark it as confidential if the platform supports it.

I ([@Blaxzter](https://github.com/Blaxzter)) will review it thoroughly and get back to you.

## Public Discussions

Please restrain from publicly discussing a potential security vulnerability. 🙊

It's better to discuss privately and try to find a solution first, to limit the potential impact as much as possible.

---

Thanks for your help!

The community and I thank you for that. 🙇
