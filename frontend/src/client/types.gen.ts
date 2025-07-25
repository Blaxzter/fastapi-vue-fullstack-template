// This file is auto-generated by @hey-api/openapi-ts

/**
 * ExampleRequest
 */
export type ExampleRequest = {
    /**
     * Name
     * The name to be processed
     */
    name: string;
    /**
     * Age
     * The age of the person, must be non-negative
     */
    age?: number | null;
};

/**
 * ExampleResponse
 */
export type ExampleResponse = {
    /**
     * Message
     * The response message
     */
    message: string;
    /**
     * Claims
     * The claims associated with the response
     */
    claims: {
        [key: string]: unknown;
    };
    /**
     * Test Value
     * A test integer value
     */
    test_value?: number | null;
};

/**
 * HTTPValidationError
 */
export type HttpValidationError = {
    /**
     * Detail
     */
    detail?: Array<ValidationError>;
};

/**
 * ValidationError
 */
export type ValidationError = {
    /**
     * Location
     */
    loc: Array<string | number>;
    /**
     * Message
     */
    msg: string;
    /**
     * Error Type
     */
    type: string;
};

export type HttpException = {
    detail: string;
};

export type TestExampleEndpointData = {
    body: ExampleRequest;
    path?: never;
    query?: never;
    url: '/api/v1/test/';
};

export type TestExampleEndpointErrors = {
    /**
     * Bad Request
     */
    400: HttpException;
    /**
     * Validation Error
     */
    422: HttpValidationError;
};

export type TestExampleEndpointError = TestExampleEndpointErrors[keyof TestExampleEndpointErrors];

export type TestExampleEndpointResponses = {
    /**
     * Successful Response
     */
    200: ExampleResponse;
};

export type TestExampleEndpointResponse = TestExampleEndpointResponses[keyof TestExampleEndpointResponses];

export type ClientOptions = {
    baseURL: 'http://localhost:8002' | (string & {});
};