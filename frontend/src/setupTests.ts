import '@testing-library/jest-dom';

// Define types for our mocks
interface CustomGlobal {
    localStorage: Storage;
    fetch: jest.Mock;
}

// Mock localStorage
const localStorageMock = {
    getItem: jest.fn(),
    setItem: jest.fn(),
    removeItem: jest.fn(),
    clear: jest.fn(),
    length: 0,
    key: jest.fn(),
} as Storage;

// Set up mocks
(globalThis as unknown as CustomGlobal).localStorage = localStorageMock;

// Mock fetch
(globalThis as unknown as CustomGlobal).fetch = jest.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({}),
        ok: true,
        status: 200,
        statusText: 'OK',
    } as Response)
);

beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
    localStorage.clear();
});

afterEach(() => {
    // Clean up after each test
    jest.resetAllMocks();
}); 