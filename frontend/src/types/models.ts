export interface Resume {
  id: number;
  name: string;
  file: File | null;
  uploadedAt: string;
  parsedText: string;
  skills: string;
  userId: number;
}

export interface Job {
  id?: string;
  title: string;
  company: string;
  location: string;
  description: string;
  url?: string;
  date_posted?: string;
  source?: string;
  skills?: string[];
  salary?: string;
}

export interface JobMatch {
  job: Job;
  tfidf_score: number;
  skill_score: number;
  matched_skills: string[];
}

export interface Bookmark {
  id: number;
  userId: number;
  jobId: number;
  createdAt: string;
}

export interface User {
  id?: number;
  username: string;
  email: string;
  firstName?: string;
  lastName?: string;
  phone?: string;
  location?: string;
  bio?: string;
  first_name?: string;  // Backend uses snake_case
  last_name?: string;   // Backend uses snake_case
  stats?: {
    resume_count: number;
    bookmark_count: number;
  };
}

export interface UserProfile {
  user: User;
  stats: {
    resumeCount: number;
    bookmarkCount: number;
  };
  resumes: Resume[];
  recentBookmarks: Bookmark[];
}

export interface Application {
  id: number;
  userId: number;
  jobId: number;
  resumeId: number;
  status: 'Applied' | 'Interview' | 'Offer' | 'Rejected';
  appliedDate: string;
  nextStep?: string;
  nextStepDate?: string;
  notes?: string;
} 