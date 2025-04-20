import { HelmetProvider } from 'react-helmet-async';
import sanitizeHtml from 'sanitize-html';
import validator from 'validator';
import React from 'react';

// Security configuration
export const securityConfig = {
  // Content Security Policy
  csp: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", 'data:', 'https:'],
    connectSrc: ["'self'", process.env.REACT_APP_API_URL || ''],
    fontSrc: ["'self'"],
    objectSrc: ["'none'"],
    mediaSrc: ["'self'"],
    frameSrc: ["'none'"],
  },

  // Input validation
  inputValidation: {
    maxLength: 1000,
    minLength: 1,
    allowedTags: ['b', 'i', 'em', 'strong', 'a'],
    allowedAttributes: {
      a: ['href', 'title', 'target'],
    },
  },

  // Rate limiting
  rateLimit: {
    requests: parseInt(process.env.REACT_APP_RATE_LIMIT_REQUESTS || '60', 10),
    minutes: parseInt(process.env.REACT_APP_RATE_LIMIT_MINUTES || '1', 10),
  },
};

// Security utilities
export const securityUtils = {
  // Sanitize HTML input
  sanitizeInput: (input: string): string => {
    return sanitizeHtml(input, {
      allowedTags: securityConfig.inputValidation.allowedTags,
      allowedAttributes: securityConfig.inputValidation.allowedAttributes,
    });
  },

  // Validate URL
  validateUrl: (url: string): boolean => {
    return validator.isURL(url, {
      protocols: ['http', 'https'],
      require_protocol: true,
    });
  },

  // Validate email
  validateEmail: (email: string): boolean => {
    return validator.isEmail(email);
  },

  // Validate input length
  validateLength: (input: string): boolean => {
    return (
      input.length >= securityConfig.inputValidation.minLength &&
      input.length <= securityConfig.inputValidation.maxLength
    );
  },
};

// Security provider component
export const SecurityProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  return <HelmetProvider>{children}</HelmetProvider>;
}; 