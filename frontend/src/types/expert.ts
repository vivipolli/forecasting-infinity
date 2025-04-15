export interface ExpertProfile {
  name: string;
  email: string;
  expertise: string[];
  socialProfiles: {
    x?: string;
    github?: string;
    linkedin?: string;
    instagram?: string;
  };
  isVerified: boolean;
  experience: string;
}

export interface ExpertVerification {
  isExpert: boolean;
  profile?: ExpertProfile;
} 