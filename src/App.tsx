/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import {
  Download,
  FolderTree,
  Database,
  Terminal,
  Layers,
  Search,
  CheckCircle2,
  Copy,
  Check,
  FileCode,
  Smartphone,
  Laptop,
  Monitor,
  Users,
  CalendarCheck,
  Award,
  BookOpen,
  FileText,
  Settings,
  ShieldCheck,
  ExternalLink,
  ChevronRight,
  UserPlus,
  Plus,
  ArrowRight,
  Filter,
  Eye,
  Trash2,
  Edit,
  GraduationCap,
  TrendingUp,
  Sparkles,
  Cloud,
  CheckCircle,
  GitBranch,
  Github,
  Globe,
  UploadCloud,
  ArrowUpRight,
} from 'lucide-react';
import { PROJECT_FILES } from './projectFiles';

export default function App() {
  const [activeTab, setActiveTab] = useState<'simulator' | 'code' | 'database' | 'setup' | 'deploy'>('simulator');
  const [githubUrlInput, setGithubUrlInput] = useState('https://github.com/YOUR_USERNAME/scholarpulse.git');
  const [selectedFile, setSelectedFile] = useState<string>('main.py');
  const [copiedFile, setCopiedFile] = useState(false);
  const [copiedSnippet, setCopiedSnippet] = useState<string | null>(null);

  // Simulator State
  const [simulatorDevice, setSimulatorDevice] = useState<'desktop' | 'tablet' | 'mobile'>('desktop');
  const [simScreen, setSimScreen] = useState<'dashboard' | 'students' | 'student_form' | 'student_details' | 'attendance' | 'marks' | 'departments' | 'reports' | 'settings'>('dashboard');
  const [simSearchTerm, setSimSearchTerm] = useState('');
  const [simDeptFilter, setSimDeptFilter] = useState('All');
  const [simSelectedStudentId, setSimSelectedStudentId] = useState<number>(1);
  const [simAttendanceDate, setSimAttendanceDate] = useState('2026-09-25');
  const [simAttendanceState, setSimAttendanceState] = useState<Record<number, 'Present' | 'Absent' | 'Late'>>({
    1: 'Present',
    2: 'Present',
    3: 'Present',
    4: 'Late',
    5: 'Present',
    6: 'Absent',
    7: 'Present',
    8: 'Present',
    9: 'Present',
    10: 'Present'
  });
  const [simMarksInput, setSimMarksInput] = useState({ score: '92.5', max: '100', subject: 'Data Structures & Algorithms', exam: 'Sem Exam' });

  // Sample data mirror
  const sampleStudents = [
    { id: 1, adm: 'ADM-2023-001', name: 'Alexander Wright', gender: 'Male', dob: '2004-03-15', email: 'a.wright@example.com', phone: '+1-555-0101', dept: 'Computer Science & Engineering', year: 2, status: 'Active', guardian: 'Robert Wright', guardianPhone: '+1-555-9101', address: '742 Evergreen Terrace, Springfield, OR', admDate: '2023-08-20' },
    { id: 2, adm: 'ADM-2023-002', name: 'Sophia Chen', gender: 'Female', dob: '2004-07-22', email: 's.chen@example.com', phone: '+1-555-0102', dept: 'Computer Science & Engineering', year: 2, status: 'Active', guardian: 'David Chen', guardianPhone: '+1-555-9102', address: '124 Conch Street, Pacific Grove, CA', admDate: '2023-08-20' },
    { id: 3, adm: 'ADM-2022-045', name: 'Marcus Johnson', gender: 'Male', dob: '2003-11-09', email: 'm.johnson@example.com', phone: '+1-555-0103', dept: 'Electrical & Electronics Engineering', year: 3, status: 'Active', guardian: 'Patricia Johnson', guardianPhone: '+1-555-9103', address: '884 Elm Avenue, Seattle, WA', admDate: '2022-08-15' },
    { id: 4, adm: 'ADM-2024-101', name: 'Elena Rodriguez', gender: 'Female', dob: '2005-01-30', email: 'e.rodriguez@example.com', phone: '+1-555-0104', dept: 'Computer Science & Engineering', year: 1, status: 'Active', guardian: 'Carlos Rodriguez', guardianPhone: '+1-555-9104', address: '312 Maple Drive, Austin, TX', admDate: '2024-08-22' },
    { id: 5, adm: 'ADM-2022-089', name: 'Liam O\'Connor', gender: 'Male', dob: '2003-05-18', email: 'l.oconnor@example.com', phone: '+1-555-0105', dept: 'Mechanical Engineering', year: 3, status: 'Active', guardian: 'Fiona O\'Connor', guardianPhone: '+1-555-9105', address: '56 Pine Street, Boston, MA', admDate: '2022-08-15' },
    { id: 6, adm: 'ADM-2024-118', name: 'Amina Patel', gender: 'Female', dob: '2005-09-12', email: 'a.patel@example.com', phone: '+1-555-0106', dept: 'Business Administration', year: 1, status: 'Active', guardian: 'Suresh Patel', guardianPhone: '+1-555-9106', address: '901 Cedar Boulevard, Denver, CO', admDate: '2024-08-22' },
    { id: 7, adm: 'ADM-2021-012', name: 'Ethan Miller', gender: 'Male', dob: '2002-12-04', email: 'e.miller@example.com', phone: '+1-555-0107', dept: 'Mechanical Engineering', year: 4, status: 'Active', guardian: 'Sarah Miller', guardianPhone: '+1-555-9107', address: '440 Birch Lane, Minneapolis, MN', admDate: '2021-08-18' },
    { id: 8, adm: 'ADM-2023-055', name: 'Chloe Dubois', gender: 'Female', dob: '2004-04-28', email: 'c.dubois@example.com', phone: '+1-555-0108', dept: 'Business Administration', year: 2, status: 'Active', guardian: 'Henri Dubois', guardianPhone: '+1-555-9108', address: '710 Oak Ridge Road, Atlanta, GA', admDate: '2023-08-20' },
  ];

  const sampleDepartments = [
    { id: 1, code: 'CS', name: 'Computer Science & Engineering', count: 4, status: 'Active', desc: 'Algorithms, software architecture, data structures, and AI systems.' },
    { id: 2, code: 'EE', name: 'Electrical & Electronics Engineering', count: 2, status: 'Active', desc: 'Circuits, embedded robotics, digital signal processing, and telecommunications.' },
    { id: 3, code: 'ME', name: 'Mechanical Engineering', count: 2, status: 'Active', desc: 'Thermodynamics, CAD manufacturing, and fluid mechanics.' },
    { id: 4, code: 'BA', name: 'Business Administration', count: 2, status: 'Active', desc: 'Financial accounting, corporate leadership, and strategic marketing.' },
  ];

  const sampleMarks = [
    { id: 1, adm: 'ADM-2023-001', name: 'Alexander Wright', subject: 'Data Structures & Algorithms', exam: 'Sem Exam', score: 92.5, max: 100, pct: 92.5, grade: 'A+' },
    { id: 2, adm: 'ADM-2023-001', name: 'Alexander Wright', subject: 'Database Systems', exam: 'Sem Exam', score: 88.0, max: 100, pct: 88.0, grade: 'A' },
    { id: 3, adm: 'ADM-2023-002', name: 'Sophia Chen', subject: 'Data Structures & Algorithms', exam: 'Sem Exam', score: 95.0, max: 100, pct: 95.0, grade: 'A+' },
    { id: 4, adm: 'ADM-2022-045', name: 'Marcus Johnson', subject: 'Digital Signal Processing', exam: 'Sem Exam', score: 78.5, max: 100, pct: 78.5, grade: 'B' },
    { id: 5, adm: 'ADM-2024-101', name: 'Elena Rodriguez', subject: 'Calculus I', exam: 'Sem Exam', score: 86.5, max: 100, pct: 86.5, grade: 'A' },
  ];

  const filteredStudents = sampleStudents.filter(s => {
    const matchesSearch = !simSearchTerm ||
      s.name.toLowerCase().includes(simSearchTerm.toLowerCase()) ||
      s.adm.toLowerCase().includes(simSearchTerm.toLowerCase()) ||
      s.phone.includes(simSearchTerm) ||
      s.dept.toLowerCase().includes(simSearchTerm.toLowerCase());
    const matchesDept = simDeptFilter === 'All' || s.dept === simDeptFilter;
    return matchesSearch && matchesDept;
  });

  const activeStudent = sampleStudents.find(s => s.id === simSelectedStudentId) || sampleStudents[0];

  const copyToClipboard = (text: string, key?: string) => {
    navigator.clipboard.writeText(text);
    if (key) {
      setCopiedSnippet(key);
      setTimeout(() => setCopiedSnippet(null), 2000);
    } else {
      setCopiedFile(true);
      setTimeout(() => setCopiedFile(false), 2000);
    }
  };

  // Grade computation helper
  const calcGrade = (score: number, max: number) => {
    if (max <= 0) return 'F';
    const pct = (score / max) * 100;
    if (pct >= 90) return 'A+';
    if (pct >= 80) return 'A';
    if (pct >= 70) return 'B';
    if (pct >= 60) return 'C';
    if (pct >= 50) return 'D';
    return 'F';
  };

  const fileKeys = Object.keys(PROJECT_FILES).sort();

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans">
      {/* Top Header */}
      <header className="bg-slate-950 border-b border-slate-800 px-6 py-4 flex flex-wrap items-center justify-between gap-4 sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-700 flex items-center justify-center text-white shadow-md shadow-blue-900/40">
            <GraduationCap className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-bold text-white tracking-tight">Student Record Management System</h1>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30">
                Python 3.11+ / MySQL / Kivy
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Native GUI Application with Parameterized SQL, Connection Pooling & ReportLab PDF
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-3">
          <a
            href="/student_record_management.zip"
            download="student_record_management.zip"
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm transition-all shadow-md shadow-emerald-950/30 active:scale-95"
          >
            <Download className="w-4 h-4" />
            <span>Download Project ZIP</span>
          </a>
        </div>
      </header>

      {/* Main Tab Navigation */}
      <nav className="bg-slate-950/80 backdrop-blur border-b border-slate-800 px-6 flex items-center gap-2 overflow-x-auto">
        <button
          onClick={() => setActiveTab('simulator')}
          className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'simulator'
              ? 'border-blue-500 text-blue-400 bg-blue-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>Interactive GUI Simulator</span>
        </button>

        <button
          onClick={() => setActiveTab('code')}
          className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'code'
              ? 'border-blue-500 text-blue-400 bg-blue-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <FolderTree className="w-4 h-4" />
          <span>Source Code Explorer ({fileKeys.length} files)</span>
        </button>

        <button
          onClick={() => setActiveTab('database')}
          className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'database'
              ? 'border-blue-500 text-blue-400 bg-blue-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Database className="w-4 h-4" />
          <span>Free Online MySQL & Architecture</span>
        </button>

        <button
          onClick={() => setActiveTab('setup')}
          className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'setup'
              ? 'border-blue-500 text-blue-400 bg-blue-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Terminal className="w-4 h-4" />
          <span>VS Code & Local Setup</span>
        </button>

        <button
          onClick={() => setActiveTab('deploy')}
          className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'deploy'
              ? 'border-blue-500 text-blue-400 bg-blue-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Github className="w-4 h-4" />
          <span>Deploy Free & GitHub Sync</span>
        </button>
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 p-6 overflow-y-auto">
        {/* TAB 1: INTERACTIVE GUI SIMULATOR */}
        {activeTab === 'simulator' && (
          <div className="space-y-4">
            {/* Simulator Toolbar */}
            <div className="flex flex-wrap items-center justify-between gap-4 bg-slate-950 p-4 rounded-xl border border-slate-800">
              <div className="flex items-center gap-3">
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Viewport Size:</span>
                <div className="flex items-center bg-slate-900 rounded-lg p-1 border border-slate-800">
                  <button
                    onClick={() => setSimulatorDevice('desktop')}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                      simulatorDevice === 'desktop' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    <Monitor className="w-3.5 h-3.5" />
                    <span>Desktop (1180px)</span>
                  </button>
                  <button
                    onClick={() => setSimulatorDevice('tablet')}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                      simulatorDevice === 'tablet' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    <Laptop className="w-3.5 h-3.5" />
                    <span>Tablet (768px)</span>
                  </button>
                  <button
                    onClick={() => setSimulatorDevice('mobile')}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                      simulatorDevice === 'mobile' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    <Smartphone className="w-3.5 h-3.5" />
                    <span>Mobile (420px)</span>
                  </button>
                </div>
              </div>

              <div className="flex items-center gap-2 text-xs text-slate-400">
                <span className="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>Native Kivy Layout Renderer Emulation (ScreenManager active)</span>
              </div>
            </div>

            {/* Simulated Native Kivy Window Frame */}
            <div className="flex justify-center">
              <div
                className={`bg-slate-100 text-slate-900 rounded-xl overflow-hidden shadow-2xl border-4 border-slate-700 transition-all duration-300 flex flex-col ${
                  simulatorDevice === 'desktop'
                    ? 'w-full max-w-6xl min-h-[680px]'
                    : simulatorDevice === 'tablet'
                    ? 'w-[768px] min-h-[640px]'
                    : 'w-[420px] min-h-[600px]'
                }`}
              >
                {/* Simulated Desktop Window Title Bar */}
                <div className="bg-[#172554] text-slate-200 px-4 py-2.5 flex items-center justify-between text-xs select-none border-b border-blue-900">
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-red-500 inline-block"></span>
                    <span className="w-2.5 h-2.5 rounded-full bg-yellow-500 inline-block"></span>
                    <span className="w-2.5 h-2.5 rounded-full bg-green-500 inline-block"></span>
                    <span className="font-semibold text-white ml-2">Student Record Management System — Kivy Native Window</span>
                  </div>
                  <span className="text-slate-400 text-[11px]">DB: MySQL 8.0 Connected</span>
                </div>

                {/* Simulated App Container (Sidebar + Content) */}
                <div className="flex-1 flex overflow-hidden">
                  {/* Sidebar (Desktop / Tablet) */}
                  {simulatorDevice !== 'mobile' && (
                    <aside className="w-56 bg-[#172554] text-slate-300 flex flex-col border-r border-blue-950 p-3 select-none flex-shrink-0">
                      <div className="mb-6 px-3 py-2.5 bg-gradient-to-br from-indigo-950/80 to-blue-950/90 rounded-xl border border-blue-800/40 shadow-sm">
                        <div className="flex items-center gap-2">
                          <div className="w-6 h-6 rounded-md bg-gradient-to-tr from-blue-500 to-teal-400 flex items-center justify-center font-black text-xs text-white shadow-sm">SP</div>
                          <div>
                            <div className="text-sm font-black text-white tracking-wide">ScholarPulse</div>
                            <div className="text-[10px] text-blue-300/80">Academic Intelligence Hub</div>
                          </div>
                        </div>
                      </div>

                      <div className="space-y-1 flex-1">
                        {[
                          { id: 'dashboard', label: 'Dashboard', icon: Layers },
                          { id: 'students', label: 'Students', icon: Users },
                          { id: 'attendance', label: 'Attendance', icon: CalendarCheck },
                          { id: 'marks', label: 'Marks & Results', icon: Award },
                          { id: 'departments', label: 'Departments', icon: BookOpen },
                          { id: 'reports', label: 'Reports', icon: FileText },
                          { id: 'settings', label: 'DB / Settings', icon: Settings },
                        ].map(item => {
                          const Icon = item.icon;
                          const isActive = simScreen === item.id || (item.id === 'students' && (simScreen === 'student_form' || simScreen === 'student_details'));
                          return (
                            <button
                              key={item.id}
                              onClick={() => setSimScreen(item.id as any)}
                              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-md text-xs font-medium transition-colors text-left ${
                                isActive
                                  ? 'bg-blue-600 text-white font-semibold shadow'
                                  : 'hover:bg-blue-900/50 text-slate-300'
                              }`}
                            >
                              <Icon className="w-4 h-4" />
                              <span>{item.label}</span>
                            </button>
                          );
                        })}
                      </div>

                      <div className="pt-3 border-t border-blue-950">
                        <div className="text-[10px] text-slate-400 px-3">
                          Logged in as: <span className="text-white font-semibold">Admin</span>
                        </div>
                      </div>
                    </aside>
                  )}

                  {/* Main Simulated Screen Content */}
                  <div className="flex-1 bg-[#F8FAFC] flex flex-col overflow-y-auto">
                    {/* Header Bar */}
                    <div className="bg-white px-6 py-3.5 border-b border-slate-200 flex items-center justify-between gap-4">
                      <div className="flex items-center gap-3">
                        {simulatorDevice === 'mobile' && (
                          <button
                            onClick={() => {
                              const screens: any[] = ['dashboard', 'students', 'attendance', 'marks', 'departments', 'reports', 'settings'];
                              const nextIdx = (screens.indexOf(simScreen) + 1) % screens.length;
                              setSimScreen(screens[nextIdx]);
                            }}
                            className="px-2 py-1 rounded bg-blue-900 text-white text-xs font-bold"
                          >
                            ☰ Menu
                          </button>
                        )}
                        <h2 className="text-base font-bold text-slate-800">
                          {simScreen === 'dashboard' && 'ScholarPulse Dashboard'}
                          {simScreen === 'students' && 'Student Registry Directory'}
                          {simScreen === 'student_form' && 'Register / Edit Student Record'}
                          {simScreen === 'student_details' && 'Student Academic Dossier'}
                          {simScreen === 'attendance' && 'Daily Attendance Audit'}
                          {simScreen === 'marks' && 'Examination Marks & Results'}
                          {simScreen === 'departments' && 'Academic Departments & Classes'}
                          {simScreen === 'reports' && 'Reports & Data Export Center'}
                          {simScreen === 'settings' && 'Database & Diagnostics'}
                        </h2>
                      </div>

                      <div className="text-xs text-slate-500 flex items-center gap-2">
                        <span>Institution Term: Fall 2026</span>
                      </div>
                    </div>

                    {/* SCREEN: DASHBOARD */}
                    {simScreen === 'dashboard' && (
                      <div className="p-6 space-y-6">
                        {/* Human Editorial Header */}
                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
                          <div>
                            <h1 className="text-xl font-semibold text-slate-900 tracking-tight">
                              ScholarPulse Dashboard
                            </h1>
                            <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500 mt-1">
                              <span>Academic Registry & Records</span>
                              <span aria-hidden="true">·</span>
                              <span>Session: Term Fall 2026</span>
                              <span aria-hidden="true">·</span>
                              <span>12 Active Student Dossiers</span>
                            </div>
                          </div>

                          <div className="flex items-center gap-2">
                            <button
                              onClick={() => setSimScreen('student_form')}
                              className="px-3.5 py-2 text-xs font-medium text-white bg-blue-700 hover:bg-blue-800 rounded-lg transition-colors flex items-center gap-1.5"
                            >
                              <Plus className="w-3.5 h-3.5" />
                              <span>+ New Student</span>
                            </button>
                            <button
                              onClick={() => setSimScreen('attendance')}
                              className="px-3.5 py-2 text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg transition-colors flex items-center gap-1.5"
                            >
                              <CalendarCheck className="w-3.5 h-3.5 text-slate-500" />
                              <span>Roll Call</span>
                            </button>
                            <button
                              onClick={() => setSimScreen('reports')}
                              className="px-3.5 py-2 text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg transition-colors flex items-center gap-1.5"
                            >
                              <FileText className="w-3.5 h-3.5 text-slate-500" />
                              <span>Export Reports</span>
                            </button>
                          </div>
                        </div>

                        {/* Metric Row: Single Elevation, 4 High-Legibility Cards, Tabular Figures */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                          <div className="bg-white p-5 rounded-lg border border-slate-200 space-y-1">
                            <div className="text-xs font-medium text-slate-500">Total Enrolled Cohort</div>
                            <div className="font-mono tabular-nums text-3xl font-semibold text-slate-900">
                              {sampleStudents.length}
                            </div>
                            <div className="text-xs text-slate-500 pt-1">
                              12 active dossiers <span aria-hidden="true">·</span> 100% in good standing
                            </div>
                          </div>

                          <div className="bg-white p-5 rounded-lg border border-slate-200 space-y-1">
                            <div className="text-xs font-medium text-slate-500">Daily Attendance Rate</div>
                            <div className="font-mono tabular-nums text-3xl font-semibold text-slate-900">
                              94.8%
                            </div>
                            <div className="text-xs text-slate-500 pt-1">
                              Roll call audited <span aria-hidden="true">·</span> Verified for today
                            </div>
                          </div>

                          <div className="bg-white p-5 rounded-lg border border-slate-200 space-y-1">
                            <div className="text-xs font-medium text-slate-500">Examination Average</div>
                            <div className="font-mono tabular-nums text-3xl font-semibold text-slate-900">
                              83.4%
                            </div>
                            <div className="text-xs text-slate-500 pt-1">
                              Semester exams average <span aria-hidden="true">·</span> 96.2% pass rate
                            </div>
                          </div>

                          <div className="bg-white p-5 rounded-lg border border-slate-200 space-y-1">
                            <div className="text-xs font-medium text-slate-500">Academic Programs</div>
                            <div className="font-mono tabular-nums text-3xl font-semibold text-slate-900">
                              {sampleDepartments.length}
                            </div>
                            <div className="text-xs text-slate-500 pt-1">
                              CS, EE, ME, BA faculties active
                            </div>
                          </div>
                        </div>

                        {/* Interactive Filtering & Search */}
                        <div className="bg-white p-4 rounded-lg border border-slate-200 space-y-3">
                          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                            {/* Segmented Filter Controls */}
                            <div className="flex items-center gap-1 p-1 bg-slate-100 rounded-lg text-xs overflow-x-auto">
                              {['All', 'Computer Science & Engineering', 'Electrical & Electronics Engineering', 'Mechanical Engineering', 'Business Administration'].map(dept => {
                                const shortLabel = dept === 'All' ? 'All Cohorts (12)' : dept === 'Computer Science & Engineering' ? 'CS (4)' : dept === 'Electrical & Electronics Engineering' ? 'EE (3)' : dept === 'Mechanical Engineering' ? 'ME (3)' : 'BA (2)';
                                const isSelected = simDeptFilter === dept;
                                return (
                                  <button
                                    key={dept}
                                    onClick={() => setSimDeptFilter(dept)}
                                    className={`px-3 py-1.5 rounded-md font-medium whitespace-nowrap transition-colors ${
                                      isSelected
                                        ? 'bg-white text-slate-900 shadow-sm'
                                        : 'text-slate-600 hover:text-slate-900'
                                    }`}
                                  >
                                    {shortLabel}
                                  </button>
                                );
                              })}
                            </div>

                            {/* Search Field */}
                            <div className="relative min-w-[220px]">
                              <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
                              <input
                                type="text"
                                placeholder="Search by name, ID, or phone..."
                                value={simSearchTerm}
                                onChange={e => setSimSearchTerm(e.target.value)}
                                className="w-full pl-9 pr-3 py-1.5 text-xs rounded-md border border-slate-200 focus:outline-none focus:ring-1 focus:ring-blue-600"
                              />
                            </div>
                          </div>

                          {/* Data Table */}
                          <div className="overflow-x-auto">
                            <table className="w-full text-left text-xs border-collapse">
                              <thead>
                                <tr className="border-b border-slate-200 text-slate-500 font-medium">
                                  <th className="py-2.5 px-3">Admission #</th>
                                  <th className="py-2.5 px-3">Student Name</th>
                                  <th className="py-2.5 px-3">Academic Program</th>
                                  <th className="py-2.5 px-3">Cohort Year</th>
                                  <th className="py-2.5 px-3">Contact Email</th>
                                  <th className="py-2.5 px-3">Status</th>
                                  <th className="py-2.5 px-3 text-right">Action</th>
                                </tr>
                              </thead>
                              <tbody className="divide-y divide-slate-100">
                                {sampleStudents
                                  .filter(st => simDeptFilter === 'All' || st.dept === simDeptFilter)
                                  .filter(st => {
                                    if (!simSearchTerm) return true;
                                    const term = simSearchTerm.toLowerCase();
                                    return st.adm.toLowerCase().includes(term) || st.name.toLowerCase().includes(term) || st.phone.includes(term) || st.dept.toLowerCase().includes(term);
                                  })
                                  .slice(0, 6)
                                  .map(st => (
                                    <tr key={st.id} className="hover:bg-slate-50/80 transition-colors">
                                      <td className="py-2.5 px-3 font-mono tabular-nums text-slate-700 font-medium">{st.adm}</td>
                                      <td className="py-2.5 px-3 font-medium text-slate-900">{st.name}</td>
                                      <td className="py-2.5 px-3 text-slate-600">{st.dept}</td>
                                      <td className="py-2.5 px-3 text-slate-600 font-mono tabular-nums">Year {st.year}</td>
                                      <td className="py-2.5 px-3 font-mono text-slate-500">{st.email}</td>
                                      <td className="py-2.5 px-3 text-emerald-700 font-medium">● {st.status}</td>
                                      <td className="py-2.5 px-3 text-right">
                                        <button
                                          onClick={() => {
                                            setSimSelectedStudentId(st.id);
                                            setSimScreen('student_details');
                                          }}
                                          className="text-blue-700 hover:text-blue-900 font-medium hover:underline"
                                        >
                                          View Profile
                                        </button>
                                      </td>
                                    </tr>
                                  ))}
                              </tbody>
                            </table>
                          </div>
                        </div>

                        {/* Administrative Quick Operations Panel */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <div className="bg-white p-4 rounded-lg border border-slate-200 space-y-2">
                            <div className="font-semibold text-slate-900 text-xs">Daily Attendance Roll Call</div>
                            <p className="text-xs text-slate-500 leading-relaxed">
                              Verify presence, mark tardiness, or log excused absences across all enrolled cohorts.
                            </p>
                            <button
                              onClick={() => setSimScreen('attendance')}
                              className="text-xs font-medium text-blue-700 hover:text-blue-900 flex items-center gap-1 pt-1"
                            >
                              <span>Open Attendance Sheet</span>
                              <ArrowRight className="w-3.5 h-3.5" />
                            </button>
                          </div>

                          <div className="bg-white p-4 rounded-lg border border-slate-200 space-y-2">
                            <div className="font-semibold text-slate-900 text-xs">Examination Gradebook</div>
                            <p className="text-xs text-slate-500 leading-relaxed">
                              Input scores, auto-compute letter grades (A+ to F), and audit semester records.
                            </p>
                            <button
                              onClick={() => setSimScreen('marks')}
                              className="text-xs font-medium text-blue-700 hover:text-blue-900 flex items-center gap-1 pt-1"
                            >
                              <span>Record Marks</span>
                              <ArrowRight className="w-3.5 h-3.5" />
                            </button>
                          </div>

                          <div className="bg-white p-4 rounded-lg border border-slate-200 space-y-2">
                            <div className="font-semibold text-slate-900 text-xs">Official Reports & Exports</div>
                            <p className="text-xs text-slate-500 leading-relaxed">
                              Export landscape PDF directories with institutional headers or raw CSV spreadsheets.
                            </p>
                            <button
                              onClick={() => setSimScreen('reports')}
                              className="text-xs font-medium text-blue-700 hover:text-blue-900 flex items-center gap-1 pt-1"
                            >
                              <span>Generate Documents</span>
                              <ArrowRight className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* SCREEN: STUDENTS DIRECTORY */}
                    {simScreen === 'students' && (
                      <div className="p-6 space-y-4">
                        {/* Search and Filters */}
                        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm space-y-3">
                          <div className="flex flex-wrap items-center gap-2">
                            <div className="relative flex-1 min-w-[200px]">
                              <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
                              <input
                                type="text"
                                placeholder="Search by Student ID, Admission #, Name, Phone..."
                                value={simSearchTerm}
                                onChange={e => setSimSearchTerm(e.target.value)}
                                className="w-full pl-9 pr-3 py-1.5 text-xs rounded border border-slate-300 focus:outline-none focus:ring-1 focus:ring-blue-600"
                              />
                            </div>

                            <select
                              value={simDeptFilter}
                              onChange={e => setSimDeptFilter(e.target.value)}
                              className="text-xs border border-slate-300 rounded px-2.5 py-1.5 bg-white text-slate-700"
                            >
                              <option value="All">All Departments</option>
                              {sampleDepartments.map(d => (
                                <option key={d.id} value={d.name}>{d.name}</option>
                              ))}
                            </select>

                            <button
                              onClick={() => {
                                setSimSearchTerm('');
                                setSimDeptFilter('All');
                              }}
                              className="px-3 py-1.5 rounded border border-slate-300 text-slate-600 hover:bg-slate-100 text-xs"
                            >
                              Reset
                            </button>

                            <button
                              onClick={() => setSimScreen('student_form')}
                              className="px-3 py-1.5 rounded bg-blue-800 text-white font-semibold text-xs hover:bg-blue-700 ml-auto"
                            >
                              + Add Student
                            </button>
                          </div>

                          <div className="text-xs text-slate-500">
                            Showing {filteredStudents.length} student record(s) matching criteria
                          </div>
                        </div>

                        {/* Student Cards List */}
                        <div className="space-y-3">
                          {filteredStudents.map(st => (
                            <div key={st.id} className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm space-y-2">
                              <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                  <span className="font-mono text-xs font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                                    {st.adm}
                                  </span>
                                  <h4 className="font-bold text-sm text-slate-900">{st.name}</h4>
                                </div>
                                <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                                  ● {st.status}
                                </span>
                              </div>

                              <div className="text-xs text-slate-600 flex flex-wrap gap-x-4 gap-y-1">
                                <span>Dept: <strong>{st.dept}</strong></span>
                                <span>Year: <strong>{st.year}</strong></span>
                                <span>Email: {st.email}</span>
                                <span>Phone: {st.phone}</span>
                              </div>

                              <div className="pt-2 flex justify-end gap-2 border-t border-slate-100">
                                <button
                                  onClick={() => {
                                    setSimSelectedStudentId(st.id);
                                    setSimScreen('student_details');
                                  }}
                                  className="px-3 py-1 text-xs rounded bg-blue-800 text-white font-medium hover:bg-blue-700"
                                >
                                  View Profile
                                </button>
                                <button
                                  onClick={() => setSimScreen('student_form')}
                                  className="px-3 py-1 text-xs rounded bg-teal-700 text-white font-medium hover:bg-teal-600"
                                >
                                  Edit
                                </button>
                                <button
                                  onClick={() => alert(`Confirm deletion of ${st.name} (${st.adm})?\nIn the real Kivy app, ConfirmDialog is shown.`)}
                                  className="px-3 py-1 text-xs rounded bg-red-600 text-white font-medium hover:bg-red-500"
                                >
                                  Delete
                                </button>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* SCREEN: STUDENT FORM (ADD / EDIT) */}
                    {simScreen === 'student_form' && (
                      <div className="p-6 space-y-5">
                        <div className="flex items-center justify-between">
                          <button
                            onClick={() => setSimScreen('students')}
                            className="text-xs text-slate-600 hover:text-slate-900 font-semibold"
                          >
                            ← Back to Directory
                          </button>
                        </div>

                        <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-5">
                          <h3 className="text-sm font-bold text-blue-900 border-b pb-2">1. Academic & Identification Information</h3>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                            <div>
                              <label className="font-semibold text-slate-700 block mb-1">Admission Number *</label>
                              <input defaultValue="ADM-2024-205" className="w-full p-2 border rounded border-slate-300" />
                            </div>
                            <div>
                              <label className="font-semibold text-slate-700 block mb-1">Department / Faculty *</label>
                              <select className="w-full p-2 border rounded border-slate-300 bg-white">
                                {sampleDepartments.map(d => (
                                  <option key={d.id} value={d.id}>{d.name}</option>
                                ))}
                              </select>
                            </div>
                            <div>
                              <label className="font-semibold text-slate-700 block mb-1">Academic Year (1-4) *</label>
                              <select className="w-full p-2 border rounded border-slate-300 bg-white">
                                <option>1</option>
                                <option>2</option>
                                <option>3</option>
                                <option>4</option>
                              </select>
                            </div>
                            <div>
                              <label className="font-semibold text-slate-700 block mb-1">Admission Date (YYYY-MM-DD) *</label>
                              <input defaultValue="2026-08-20" className="w-full p-2 border rounded border-slate-300" />
                            </div>
                          </div>

                          <h3 className="text-sm font-bold text-blue-900 border-b pb-2 pt-2">2. Personal Information</h3>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                            <div>
                              <label className="font-semibold text-slate-700 block mb-1">First Name *</label>
                              <input defaultValue="Lucas" className="w-full p-2 border rounded border-slate-300" />
                            </div>
                            <div>
                              <label className="font-semibold text-slate-700 block mb-1">Last Name *</label>
                              <input defaultValue="Vance" className="w-full p-2 border rounded border-slate-300" />
                            </div>
                            <div>
                              <label className="font-semibold text-slate-700 block mb-1">Gender *</label>
                              <select className="w-full p-2 border rounded border-slate-300 bg-white">
                                <option>Male</option>
                                <option>Female</option>
                                <option>Other</option>
                              </select>
                            </div>
                            <div>
                              <label className="font-semibold text-slate-700 block mb-1">Date of Birth (YYYY-MM-DD) *</label>
                              <input defaultValue="2005-04-18" className="w-full p-2 border rounded border-slate-300" />
                            </div>
                          </div>

                          <h3 className="text-sm font-bold text-blue-900 border-b pb-2 pt-2">3. Contact & Guardian Details</h3>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                            <div>
                              <label className="font-semibold text-slate-700 block mb-1">Email Address *</label>
                              <input defaultValue="l.vance@example.com" className="w-full p-2 border rounded border-slate-300" />
                            </div>
                            <div>
                              <label className="font-semibold text-slate-700 block mb-1">Phone Number *</label>
                              <input defaultValue="+1-555-0199" className="w-full p-2 border rounded border-slate-300" />
                            </div>
                            <div>
                              <label className="font-semibold text-slate-700 block mb-1">Guardian Name *</label>
                              <input defaultValue="Mark Vance" className="w-full p-2 border rounded border-slate-300" />
                            </div>
                            <div>
                              <label className="font-semibold text-slate-700 block mb-1">Guardian Phone *</label>
                              <input defaultValue="+1-555-9199" className="w-full p-2 border rounded border-slate-300" />
                            </div>
                            <div className="md:col-span-2">
                              <label className="font-semibold text-slate-700 block mb-1">Residential Street Address *</label>
                              <input defaultValue="500 Meadow Lane, Portland, OR" className="w-full p-2 border rounded border-slate-300" />
                            </div>
                          </div>

                          <div className="flex gap-3 pt-3 border-t">
                            <button
                              onClick={() => {
                                alert('Student record successfully saved into MySQL!');
                                setSimScreen('students');
                              }}
                              className="px-5 py-2 rounded bg-blue-800 text-white font-bold text-xs hover:bg-blue-700"
                            >
                              Save Student Record
                            </button>
                            <button
                              onClick={() => setSimScreen('students')}
                              className="px-4 py-2 rounded border border-slate-300 text-slate-600 text-xs hover:bg-slate-100"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* SCREEN: STUDENT DETAILS (PROFILE) */}
                    {simScreen === 'student_details' && (
                      <div className="p-6 space-y-4">
                        <button
                          onClick={() => setSimScreen('students')}
                          className="text-xs text-slate-600 hover:text-slate-900 font-semibold"
                        >
                          ← Back to Directory
                        </button>

                        {/* Profile Header Banner */}
                        <div className="bg-[#172554] text-white p-5 rounded-lg flex items-center justify-between">
                          <div>
                            <div className="flex items-center gap-3">
                              <h3 className="text-lg font-black">{activeStudent.name}</h3>
                              <span className="bg-blue-700 text-white text-xs px-2 py-0.5 rounded font-mono">
                                {activeStudent.adm}
                              </span>
                            </div>
                            <div className="text-xs text-blue-200 mt-1">
                              {activeStudent.dept} | Year {activeStudent.year} | Status: {activeStudent.status}
                            </div>
                          </div>

                          <div className="text-right">
                            <div className="text-[10px] text-blue-300 uppercase font-bold">Attendance Rate</div>
                            <div className="text-2xl font-black text-emerald-400">92.0%</div>
                          </div>
                        </div>

                        {/* Dossier Cards */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm space-y-2.5 text-xs">
                            <h4 className="font-bold text-blue-900 border-b pb-1.5">Personal & Contact</h4>
                            <div className="flex justify-between py-1 border-b border-slate-100">
                              <span className="text-slate-500">Gender</span>
                              <span className="font-semibold text-slate-800">{activeStudent.gender}</span>
                            </div>
                            <div className="flex justify-between py-1 border-b border-slate-100">
                              <span className="text-slate-500">Date of Birth</span>
                              <span className="font-semibold text-slate-800">{activeStudent.dob}</span>
                            </div>
                            <div className="flex justify-between py-1 border-b border-slate-100">
                              <span className="text-slate-500">Email</span>
                              <span className="font-semibold text-slate-800">{activeStudent.email}</span>
                            </div>
                            <div className="flex justify-between py-1 border-b border-slate-100">
                              <span className="text-slate-500">Phone</span>
                              <span className="font-semibold text-slate-800">{activeStudent.phone}</span>
                            </div>
                            <div className="flex justify-between py-1">
                              <span className="text-slate-500">Address</span>
                              <span className="font-semibold text-slate-800 text-right">{activeStudent.address}</span>
                            </div>
                          </div>

                          <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm space-y-2.5 text-xs">
                            <h4 className="font-bold text-blue-900 border-b pb-1.5">Academic & Guardian</h4>
                            <div className="flex justify-between py-1 border-b border-slate-100">
                              <span className="text-slate-500">Department</span>
                              <span className="font-semibold text-slate-800">{activeStudent.dept}</span>
                            </div>
                            <div className="flex justify-between py-1 border-b border-slate-100">
                              <span className="text-slate-500">Academic Year</span>
                              <span className="font-semibold text-slate-800">Year {activeStudent.year}</span>
                            </div>
                            <div className="flex justify-between py-1 border-b border-slate-100">
                              <span className="text-slate-500">Admission Date</span>
                              <span className="font-semibold text-slate-800">{activeStudent.admDate}</span>
                            </div>
                            <div className="flex justify-between py-1 border-b border-slate-100">
                              <span className="text-slate-500">Guardian Name</span>
                              <span className="font-semibold text-slate-800">{activeStudent.guardian}</span>
                            </div>
                            <div className="flex justify-between py-1">
                              <span className="text-slate-500">Guardian Phone</span>
                              <span className="font-semibold text-slate-800">{activeStudent.guardianPhone}</span>
                            </div>
                          </div>
                        </div>

                        {/* Recent Marks Transcript */}
                        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm space-y-2">
                          <h4 className="font-bold text-xs text-blue-900">Academic Marks Record</h4>
                          <div className="divide-y text-xs">
                            {sampleMarks.filter(m => m.adm === activeStudent.adm).map(m => (
                              <div key={m.id} className="py-2 flex items-center justify-between">
                                <div>
                                  <span className="font-semibold text-slate-800">{m.subject}</span>
                                  <span className="text-slate-400 ml-2">({m.exam})</span>
                                </div>
                                <div className="flex items-center gap-3">
                                  <span>{m.score} / {m.max} ({m.pct}%)</span>
                                  <span className="font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded">
                                    Grade: {m.grade}
                                  </span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}

                    {/* SCREEN: ATTENDANCE */}
                    {simScreen === 'attendance' && (
                      <div className="p-6 space-y-4">
                        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3 text-xs">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-slate-700">Attendance Date:</span>
                            <input
                              type="date"
                              value={simAttendanceDate}
                              onChange={e => setSimAttendanceDate(e.target.value)}
                              className="border rounded p-1.5 bg-white text-slate-800"
                            />
                            <button
                              onClick={() => {
                                const allPres: any = {};
                                sampleStudents.forEach(s => { allPres[s.id] = 'Present'; });
                                setSimAttendanceState(allPres);
                              }}
                              className="px-3 py-1.5 bg-emerald-700 hover:bg-emerald-600 text-white rounded font-semibold"
                            >
                              Mark All Present
                            </button>
                          </div>

                          <button
                            onClick={() => alert(`Attendance successfully committed for date ${simAttendanceDate}!`)}
                            className="px-4 py-1.5 bg-blue-900 hover:bg-blue-800 text-white font-bold rounded"
                          >
                            Save All Attendance
                          </button>
                        </div>

                        {/* Roll Call Table */}
                        <div className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden text-xs">
                          <table className="w-full text-left">
                            <thead className="bg-slate-100 text-slate-700 border-b">
                              <tr>
                                <th className="p-3">Admission No</th>
                                <th className="p-3">Student Name</th>
                                <th className="p-3">Department</th>
                                <th className="p-3">Status</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                              {sampleStudents.map(st => {
                                const currentStatus = simAttendanceState[st.id] || 'Present';
                                return (
                                  <tr key={st.id} className="hover:bg-slate-50">
                                    <td className="p-3 font-mono font-bold text-blue-700">{st.adm}</td>
                                    <td className="p-3 font-semibold text-slate-800">{st.name}</td>
                                    <td className="p-3 text-slate-600">{st.dept}</td>
                                    <td className="p-3">
                                      <div className="flex items-center gap-1.5">
                                        {(['Present', 'Absent', 'Late'] as const).map(stat => (
                                          <button
                                            key={stat}
                                            onClick={() => setSimAttendanceState(prev => ({ ...prev, [st.id]: stat }))}
                                            className={`px-2 py-0.5 rounded text-[11px] font-bold transition-all ${
                                              currentStatus === stat
                                                ? stat === 'Present'
                                                  ? 'bg-emerald-600 text-white'
                                                  : stat === 'Absent'
                                                  ? 'bg-red-600 text-white'
                                                  : 'bg-amber-600 text-white'
                                                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                            }`}
                                          >
                                            {stat}
                                          </button>
                                        ))}
                                      </div>
                                    </td>
                                  </tr>
                                );
                              })}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    )}

                    {/* SCREEN: MARKS & RESULTS */}
                    {simScreen === 'marks' && (
                      <div className="p-6 space-y-4">
                        {/* Score Entry Card */}
                        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm space-y-3 text-xs">
                          <h4 className="font-bold text-sm text-blue-900">Score & Grade Entry</h4>
                          <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
                            <div>
                              <label className="block text-slate-600 mb-1">Student</label>
                              <select className="w-full p-2 border rounded bg-white">
                                {sampleStudents.map(s => (
                                  <option key={s.id} value={s.id}>{s.adm} - {s.name}</option>
                                ))}
                              </select>
                            </div>
                            <div>
                              <label className="block text-slate-600 mb-1">Subject</label>
                              <input
                                value={simMarksInput.subject}
                                onChange={e => setSimMarksInput({ ...simMarksInput, subject: e.target.value })}
                                className="w-full p-2 border rounded"
                              />
                            </div>
                            <div>
                              <label className="block text-slate-600 mb-1">Exam Type</label>
                              <select
                                value={simMarksInput.exam}
                                onChange={e => setSimMarksInput({ ...simMarksInput, exam: e.target.value })}
                                className="w-full p-2 border rounded bg-white"
                              >
                                <option value="Quiz 1">Quiz 1</option>
                                <option value="Quiz 2">Quiz 2</option>
                                <option value="Sem Exam">Sem Exam</option>
                                <option value="Final Exam">Final Exam</option>
                                <option value="Lab Practical">Lab Practical</option>
                                <option value="Final Project">Final Project</option>
                                <option value="Assignment">Assignment</option>
                              </select>
                            </div>
                            <div>
                              <label className="block text-slate-600 mb-1">Score Obtained</label>
                              <input
                                value={simMarksInput.score}
                                onChange={e => setSimMarksInput({ ...simMarksInput, score: e.target.value })}
                                className="w-full p-2 border rounded"
                              />
                            </div>
                            <div>
                              <label className="block text-slate-600 mb-1">Max Score</label>
                              <input
                                value={simMarksInput.max}
                                onChange={e => setSimMarksInput({ ...simMarksInput, max: e.target.value })}
                                className="w-full p-2 border rounded"
                              />
                            </div>
                          </div>

                          <div className="flex items-center justify-between pt-2">
                            <div className="text-xs">
                              Live Grade Preview:{' '}
                              <strong className="text-blue-700 text-sm">
                                {calcGrade(parseFloat(simMarksInput.score) || 0, parseFloat(simMarksInput.max) || 100)} (
                                {(((parseFloat(simMarksInput.score) || 0) / (parseFloat(simMarksInput.max) || 100)) * 100).toFixed(1)}%)
                              </strong>
                            </div>
                            <button
                              onClick={() => alert('Marks record saved with calculated grade!')}
                              className="px-4 py-2 bg-blue-800 text-white font-bold rounded hover:bg-blue-700"
                            >
                              Record Score
                            </button>
                          </div>
                        </div>

                        {/* Recorded Scores Table */}
                        <div className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden text-xs">
                          <table className="w-full text-left">
                            <thead className="bg-slate-100 text-slate-700 border-b">
                              <tr>
                                <th className="p-3">Student</th>
                                <th className="p-3">Subject</th>
                                <th className="p-3">Exam</th>
                                <th className="p-3">Score</th>
                                <th className="p-3">Grade</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                              {sampleMarks.map(m => (
                                <tr key={m.id} className="hover:bg-slate-50">
                                  <td className="p-3 font-semibold text-slate-800">{m.adm} - {m.name}</td>
                                  <td className="p-3 text-slate-600">{m.subject}</td>
                                  <td className="p-3 text-slate-600">{m.exam}</td>
                                  <td className="p-3 font-mono font-bold text-slate-800">{m.score} / {m.max}</td>
                                  <td className="p-3 font-bold text-blue-700">{m.grade} ({m.pct}%)</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    )}

                    {/* SCREEN: DEPARTMENTS */}
                    {simScreen === 'departments' && (
                      <div className="p-6 space-y-4 text-xs">
                        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm flex justify-between items-center">
                          <div>
                            <h4 className="font-bold text-sm text-slate-800">Academic Faculties & Departments</h4>
                            <p className="text-slate-500">Foreign key relationships ensure student integrity</p>
                          </div>
                          <button
                            onClick={() => alert('Department creation dialog opened!')}
                            className="px-3 py-1.5 bg-blue-800 text-white font-semibold rounded"
                          >
                            + Add Department
                          </button>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {sampleDepartments.map(dept => (
                            <div key={dept.id} className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm space-y-2">
                              <div className="flex items-center justify-between">
                                <span className="font-mono font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded">
                                  {dept.code}
                                </span>
                                <span className="font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
                                  ● {dept.status}
                                </span>
                              </div>
                              <h5 className="font-bold text-sm text-slate-900">{dept.name}</h5>
                              <p className="text-slate-500 text-[11px]">{dept.desc}</p>
                              <div className="pt-2 border-t flex justify-between items-center text-slate-600">
                                <span>Enrolled: <strong>{dept.count} students</strong></span>
                                <span className="text-[11px] text-blue-600 font-semibold cursor-pointer">Edit Details</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* SCREEN: REPORTS */}
                    {simScreen === 'reports' && (
                      <div className="p-6 space-y-4 text-xs">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-3">
                            <div className="flex justify-between items-center">
                              <h4 className="font-bold text-sm text-slate-900">Official Student Directory (PDF)</h4>
                              <span className="bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded text-[10px]">
                                ReportLab PDF
                              </span>
                            </div>
                            <p className="text-slate-500">
                              Produces landscape formatted document with institutional header, page numbers, and complete student directory.
                            </p>
                            <button
                              onClick={() => alert('PDF generation initiated! Saved to reports_export/ directory.')}
                              className="w-full py-2 bg-blue-800 hover:bg-blue-700 text-white font-bold rounded"
                            >
                              Generate PDF Report
                            </button>
                          </div>

                          <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-3">
                            <div className="flex justify-between items-center">
                              <h4 className="font-bold text-sm text-slate-900">Student Registry Export (CSV)</h4>
                              <span className="bg-teal-100 text-teal-800 font-bold px-2 py-0.5 rounded text-[10px]">
                                CSV Spreadsheet
                              </span>
                            </div>
                            <p className="text-slate-500">
                              Tabular format containing all contact, guardian, and enrollment columns for Microsoft Excel.
                            </p>
                            <button
                              onClick={() => alert('CSV file successfully exported to reports_export/students_export.csv!')}
                              className="w-full py-2 bg-teal-700 hover:bg-teal-600 text-white font-bold rounded"
                            >
                              Export CSV Spreadsheet
                            </button>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* SCREEN: SETTINGS */}
                    {simScreen === 'settings' && (
                      <div className="p-6 space-y-4 text-xs">
                        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm space-y-2">
                          <div className="flex items-center gap-2 text-emerald-700 font-bold text-sm">
                            <CheckCircle2 className="w-4 h-4" />
                            <span>Free Online Cloud MySQL Connected</span>
                          </div>
                          <p className="text-slate-600">
                            The application connects directly to remote cloud MySQL over standard wire protocol with SSL and auto-reconnect pooling. No local server or desktop MySQL Workbench required!
                          </p>
                          <div className="inline-block mt-1 font-mono text-[11px] bg-emerald-50 text-emerald-800 px-2.5 py-1 rounded border border-emerald-200">
                            Auto-provision tables: python init_database.py
                          </div>
                        </div>

                        <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-sm space-y-2">
                          <h4 className="font-bold text-slate-800 text-sm">Active .env Configuration</h4>
                          <div className="space-y-1 font-mono text-[11px] text-slate-600 bg-slate-50 p-3 rounded">
                            <div>DB_HOST = mysql-instance.aivencloud.com</div>
                            <div>DB_PORT = 3306</div>
                            <div>DB_NAME = defaultdb</div>
                            <div>DB_USER = avnadmin</div>
                            <div>DB_PASSWORD = ••••••••••••</div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: CODE EXPLORER */}
        {activeTab === 'code' && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {/* File List Tree */}
            <div className="bg-slate-950 rounded-xl border border-slate-800 p-4 space-y-2">
              <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 px-2">
                Project Files ({fileKeys.length})
              </div>
              <div className="space-y-1 max-h-[640px] overflow-y-auto pr-1">
                {fileKeys.map(filePath => {
                  const isSelected = selectedFile === filePath;
                  return (
                    <button
                      key={filePath}
                      onClick={() => setSelectedFile(filePath)}
                      className={`w-full flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-mono transition-colors text-left truncate ${
                        isSelected
                          ? 'bg-blue-600 text-white font-semibold'
                          : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                      }`}
                    >
                      <FileCode className="w-3.5 h-3.5 flex-shrink-0" />
                      <span className="truncate">{filePath}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Code Content Viewer */}
            <div className="md:col-span-3 bg-slate-950 rounded-xl border border-slate-800 overflow-hidden flex flex-col">
              <div className="px-5 py-3 bg-slate-900/80 border-b border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-2 font-mono text-xs text-blue-400">
                  <FileCode className="w-4 h-4" />
                  <span>student_record_management/{selectedFile}</span>
                </div>
                <button
                  onClick={() => copyToClipboard(PROJECT_FILES[selectedFile] || '')}
                  className="flex items-center gap-1.5 px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs transition-colors"
                >
                  {copiedFile ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copiedFile ? 'Copied!' : 'Copy Code'}</span>
                </button>
              </div>

              <div className="p-4 overflow-x-auto max-h-[640px] font-mono text-xs leading-relaxed text-slate-300">
                <pre>{PROJECT_FILES[selectedFile] || '(Empty file or not found)'}</pre>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: FREE ONLINE MYSQL & ARCHITECTURE */}
        {activeTab === 'database' && (
          <div className="space-y-6">
            {/* Free Cloud MySQL Setup Guide Banner */}
            <div className="bg-gradient-to-r from-slate-950 via-slate-900 to-blue-950 p-6 rounded-xl border border-blue-900/50 space-y-4 shadow-lg">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-2 text-xs font-bold uppercase text-cyan-400">
                    <Cloud className="w-4 h-4" />
                    <span>Free Online Cloud MySQL Setup</span>
                  </div>
                  <h3 className="text-lg font-black text-white mt-1">Zero Workbench Required — Connect in Minutes</h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Connect directly to free online cloud-hosted MySQL databases without installing MySQL Workbench or desktop database software.
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5">
                    <CheckCircle className="w-3.5 h-3.5" />
                    <span>1-Click Auto Provisioning</span>
                  </span>
                </div>
              </div>

              {/* Free Providers Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div className="bg-slate-900/90 p-4 rounded-lg border border-slate-800 space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-xs text-white">1. Aiven.io (Recommended)</span>
                    <span className="text-[10px] bg-blue-500/20 text-blue-300 px-1.5 py-0.5 rounded">Free Tier</span>
                  </div>
                  <p className="text-[11px] text-slate-400 leading-relaxed">
                    Free managed MySQL 8.0 cloud database. Generates Host, Port, DB, User, and Password instantly.
                  </p>
                </div>

                <div className="bg-slate-900/90 p-4 rounded-lg border border-slate-800 space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-xs text-white">2. TiDB Cloud Serverless</span>
                    <span className="text-[10px] bg-teal-500/20 text-teal-300 px-1.5 py-0.5 rounded">Free Forever</span>
                  </div>
                  <p className="text-[11px] text-slate-400 leading-relaxed">
                    Serverless MySQL-compatible database. Includes built-in browser web SQL editor.
                  </p>
                </div>

                <div className="bg-slate-900/90 p-4 rounded-lg border border-slate-800 space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-xs text-white">3. Clever Cloud / Alwaysdata</span>
                    <span className="text-[10px] bg-indigo-500/20 text-indigo-300 px-1.5 py-0.5 rounded">Free MySQL</span>
                  </div>
                  <p className="text-[11px] text-slate-400 leading-relaxed">
                    Provides free cloud MySQL with integrated online phpMyAdmin web management.
                  </p>
                </div>
              </div>

              {/* 1-Click Provisioning Command Box */}
              <div className="bg-slate-950 p-4 rounded-lg border border-blue-900/40 flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div className="space-y-1">
                  <div className="text-xs font-bold text-slate-200 flex items-center gap-1.5">
                    <Terminal className="w-3.5 h-3.5 text-blue-400" />
                    <span>Run Automated Remote Initializer (No Workbench Needed!)</span>
                  </div>
                  <div className="text-[11px] text-slate-400">
                    After adding your remote cloud host to <code>.env</code>, run this in VS Code to auto-build tables and seed sample data:
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <code className="text-xs font-mono text-emerald-400 bg-slate-900 px-3 py-1.5 rounded border border-slate-700">
                    python init_database.py
                  </code>
                  <button
                    onClick={() => copyToClipboard('python init_database.py', 'initdb')}
                    className="px-2.5 py-1.5 rounded bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium transition-colors"
                  >
                    {copiedSnippet === 'initdb' ? 'Copied!' : 'Copy'}
                  </button>
                </div>
              </div>
            </div>

            {/* ER Diagram Overview */}
            <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-base font-bold text-white">Relational Database Architecture</h3>
                  <p className="text-xs text-slate-400">InnoDB Engine, UTF-8mb4, Normalized Foreign Keys, Cascades & Secondary Indexes</p>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
                  4 Normalized Entities
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2">
                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
                  <div className="font-bold text-xs text-blue-400 uppercase">1. departments</div>
                  <ul className="text-xs font-mono text-slate-400 space-y-1">
                    <li className="text-white font-semibold">● id (PK, INT AUTO_INC)</li>
                    <li>● code (VARCHAR(20) UNIQUE)</li>
                    <li>● name (VARCHAR(100) UNIQUE)</li>
                    <li>● description (TEXT)</li>
                    <li>● status (ENUM)</li>
                  </ul>
                </div>

                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
                  <div className="font-bold text-xs text-blue-400 uppercase">2. students</div>
                  <ul className="text-xs font-mono text-slate-400 space-y-1">
                    <li className="text-white font-semibold">● id (PK, INT AUTO_INC)</li>
                    <li className="text-blue-300">● admission_number (UNIQUE)</li>
                    <li>● first_name, last_name</li>
                    <li>● gender, date_of_birth</li>
                    <li>● email (UNIQUE), phone</li>
                    <li className="text-amber-400 font-semibold">● department_id (FK → departments)</li>
                    <li>● year, guardian info</li>
                    <li>● status (Active/Inactive)</li>
                  </ul>
                </div>

                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
                  <div className="font-bold text-xs text-blue-400 uppercase">3. attendance</div>
                  <ul className="text-xs font-mono text-slate-400 space-y-1">
                    <li className="text-white font-semibold">● id (PK, INT AUTO_INC)</li>
                    <li className="text-amber-400 font-semibold">● student_id (FK → students)</li>
                    <li>● attendance_date (DATE)</li>
                    <li>● status (Present/Absent/Late)</li>
                    <li>● remarks (VARCHAR(255))</li>
                    <li className="text-blue-300">● UNIQUE(student_id, date)</li>
                  </ul>
                </div>

                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
                  <div className="font-bold text-xs text-blue-400 uppercase">4. marks</div>
                  <ul className="text-xs font-mono text-slate-400 space-y-1">
                    <li className="text-white font-semibold">● id (PK, INT AUTO_INC)</li>
                    <li className="text-amber-400 font-semibold">● student_id (FK → students)</li>
                    <li>● subject (VARCHAR(100))</li>
                    <li>● exam_name (VARCHAR(100))</li>
                    <li>● marks_obtained, max_marks</li>
                    <li>● percentage, grade</li>
                    <li className="text-blue-300">● UNIQUE(student, subject, exam)</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* SQL Schema Script Viewer */}
            <div className="bg-slate-950 rounded-xl border border-slate-800 overflow-hidden">
              <div className="px-5 py-3.5 bg-slate-900/80 border-b border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-2 text-xs font-bold text-slate-200">
                  <Database className="w-4 h-4 text-blue-400" />
                  <span>database/schema.sql (DDL Script)</span>
                </div>
                <button
                  onClick={() => copyToClipboard(PROJECT_FILES['database/schema.sql'] || '', 'schema')}
                  className="flex items-center gap-1.5 px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-xs text-slate-200"
                >
                  {copiedSnippet === 'schema' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copiedSnippet === 'schema' ? 'Copied SQL!' : 'Copy schema.sql'}</span>
                </button>
              </div>
              <div className="p-4 max-h-80 overflow-y-auto font-mono text-xs text-slate-300">
                <pre>{PROJECT_FILES['database/schema.sql']}</pre>
              </div>
            </div>

            {/* SQL Seed Script Viewer */}
            <div className="bg-slate-950 rounded-xl border border-slate-800 overflow-hidden">
              <div className="px-5 py-3.5 bg-slate-900/80 border-b border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-2 text-xs font-bold text-slate-200">
                  <Database className="w-4 h-4 text-teal-400" />
                  <span>database/seed.sql (Sample Seed Records)</span>
                </div>
                <button
                  onClick={() => copyToClipboard(PROJECT_FILES['database/seed.sql'] || '', 'seed')}
                  className="flex items-center gap-1.5 px-3 py-1 rounded bg-slate-800 hover:bg-slate-700 text-xs text-slate-200"
                >
                  {copiedSnippet === 'seed' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copiedSnippet === 'seed' ? 'Copied SQL!' : 'Copy seed.sql'}</span>
                </button>
              </div>
              <div className="p-4 max-h-80 overflow-y-auto font-mono text-xs text-slate-300">
                <pre>{PROJECT_FILES['database/seed.sql']}</pre>
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: SETUP GUIDE & VS CODE */}
        {activeTab === 'setup' && (
          <div className="space-y-6 max-w-4xl mx-auto">
            {/* Quick Run Card */}
            <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 space-y-4">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Terminal className="w-5 h-5 text-blue-400" />
                <span>Running in Visual Studio Code (3-Step Quickstart)</span>
              </h3>

              <div className="space-y-3">
                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
                  <div className="flex justify-between items-center text-xs text-slate-400 font-semibold">
                    <span>1. Create Virtual Environment & Activate</span>
                    <button
                      onClick={() => copyToClipboard('python -m venv .venv\n# Windows:\n.venv\\Scripts\\activate\n# macOS/Linux:\nsource .venv/bin/activate', 'step1')}
                      className="text-blue-400 hover:text-blue-300 text-[11px]"
                    >
                      {copiedSnippet === 'step1' ? 'Copied!' : 'Copy Command'}
                    </button>
                  </div>
                  <pre className="text-xs font-mono text-emerald-400 bg-slate-950 p-2.5 rounded">
{`# Create virtual environment
python -m venv .venv

# Windows activation:
.venv\\Scripts\\activate

# Linux / macOS activation:
source .venv/bin/activate`}
                  </pre>
                </div>

                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
                  <div className="flex justify-between items-center text-xs text-slate-400 font-semibold">
                    <span>2. Install Dependencies</span>
                    <button
                      onClick={() => copyToClipboard('pip install -r requirements.txt', 'step2')}
                      className="text-blue-400 hover:text-blue-300 text-[11px]"
                    >
                      {copiedSnippet === 'step2' ? 'Copied!' : 'Copy Command'}
                    </button>
                  </div>
                  <pre className="text-xs font-mono text-emerald-400 bg-slate-950 p-2.5 rounded">
pip install -r requirements.txt
                  </pre>
                </div>

                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
                  <div className="flex justify-between items-center text-xs text-slate-400 font-semibold">
                    <span>3. Initialize Free Online MySQL Database (Zero Workbench Needed!)</span>
                    <button
                      onClick={() => copyToClipboard('python init_database.py', 'step3')}
                      className="text-blue-400 hover:text-blue-300 text-[11px]"
                    >
                      {copiedSnippet === 'step3' ? 'Copied!' : 'Copy Command'}
                    </button>
                  </div>
                  <pre className="text-xs font-mono text-emerald-400 bg-slate-950 p-2.5 rounded">
# Automatically builds all tables and inserts seed records on your free cloud database:
python init_database.py
                  </pre>
                </div>

                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
                  <div className="flex justify-between items-center text-xs text-slate-400 font-semibold">
                    <span>4. Launch the Native Desktop Application</span>
                    <button
                      onClick={() => copyToClipboard('python main.py', 'step4')}
                      className="text-blue-400 hover:text-blue-300 text-[11px]"
                    >
                      {copiedSnippet === 'step4' ? 'Copied!' : 'Copy Command'}
                    </button>
                  </div>
                  <pre className="text-xs font-mono text-emerald-400 bg-slate-950 p-2.5 rounded">
python main.py
                  </pre>
                </div>
              </div>
            </div>

            {/* Cloud MySQL Configuration */}
            <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 space-y-4">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <Database className="w-5 h-5 text-teal-400" />
                <span>Configuring Cloud MySQL Database</span>
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Copy <code>.env.example</code> to <code>.env</code>. You can use any free online hosted MySQL cloud service (e.g. <strong>Aiven.io</strong>, <strong>TiDB Cloud</strong>, <strong>Clever Cloud</strong>, <strong>Alwaysdata</strong>). No MySQL Workbench or desktop database software is needed!
              </p>

              <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
                <div className="flex justify-between items-center text-xs text-slate-400">
                  <span className="font-semibold">.env Configuration Template</span>
                  <button
                    onClick={() => copyToClipboard(PROJECT_FILES['.env.example'] || '', 'env')}
                    className="text-blue-400 hover:text-blue-300 text-[11px]"
                  >
                    {copiedSnippet === 'env' ? 'Copied!' : 'Copy .env Template'}
                  </button>
                </div>
                <pre className="text-xs font-mono text-slate-300 bg-slate-950 p-3 rounded">
{`DB_HOST=your-mysql-hostname.aivencloud.com
DB_PORT=3306
DB_NAME=defaultdb
DB_USER=avnadmin
DB_PASSWORD=your_secure_password`}
                </pre>
              </div>
            </div>
          </div>
        )}

        {/* TAB 5: DEPLOY TO FREE CLOUD & GITHUB SYNC */}
        {activeTab === 'deploy' && (
          <div className="space-y-6 max-w-4xl mx-auto">
            {/* GitHub Setup & Push */}
            <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 space-y-5">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-slate-900 border border-slate-700 flex items-center justify-center text-white">
                    <Github className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-white">1. Create & Push to GitHub Repository</h3>
                    <p className="text-xs text-slate-400">Local git repository is initialized on branch <code>main</code> with all files staged and committed.</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono px-2.5 py-1 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    Git Initialized (Branch: main)
                  </span>
                </div>
              </div>

              {/* Step 1: Create Repo on GitHub */}
              <div className="space-y-2">
                <div className="text-xs font-semibold text-slate-200">Step 1: Create a new repository on your GitHub account</div>
                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div className="text-xs text-slate-400 leading-relaxed">
                    Go to <strong>github.com/new</strong>, enter a repository name (e.g. <code>scholarpulse-srm</code>), choose Public or Private, and leave "Initialize with README" unchecked (already included).
                  </div>
                  <a
                    href="https://github.com/new"
                    target="_blank"
                    rel="noreferrer"
                    className="px-3.5 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium whitespace-nowrap flex items-center gap-1.5 transition-colors self-start sm:self-auto"
                  >
                    <span>Open GitHub New Repo</span>
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>

              {/* Step 2: Push Commands */}
              <div className="space-y-2">
                <div className="text-xs font-semibold text-slate-200">Step 2: Enter your GitHub Repository URL to generate push commands:</div>
                <div className="flex items-center gap-2">
                  <input
                    type="text"
                    value={githubUrlInput}
                    onChange={e => setGithubUrlInput(e.target.value)}
                    placeholder="https://github.com/yourusername/scholarpulse-srm.git"
                    className="flex-1 px-3.5 py-2 text-xs font-mono rounded-lg bg-slate-900 border border-slate-700 text-slate-200 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                </div>

                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2 mt-2">
                  <div className="flex justify-between items-center text-xs text-slate-400">
                    <span className="font-semibold">Terminal Commands (Run in VS Code terminal)</span>
                    <button
                      onClick={() => copyToClipboard(`git remote add origin ${githubUrlInput}\ngit branch -M main\ngit push -u origin main`, 'pushcmd')}
                      className="text-blue-400 hover:text-blue-300 text-[11px]"
                    >
                      {copiedSnippet === 'pushcmd' ? 'Copied Commands!' : 'Copy Push Commands'}
                    </button>
                  </div>
                  <pre className="text-xs font-mono text-emerald-400 bg-slate-950 p-3 rounded overflow-x-auto">
{`git remote add origin ${githubUrlInput || 'https://github.com/YOUR_USERNAME/YOUR_REPO.git'}
git branch -M main
git push -u origin main`}
                  </pre>
                </div>

                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2">
                  <div className="flex justify-between items-center text-xs text-slate-400">
                    <span className="font-semibold">Or Use Automated Helper Script:</span>
                    <button
                      onClick={() => copyToClipboard(`./push_to_github.sh ${githubUrlInput}`, 'scriptcmd')}
                      className="text-blue-400 hover:text-blue-300 text-[11px]"
                    >
                      {copiedSnippet === 'scriptcmd' ? 'Copied Script!' : 'Copy Script Command'}
                    </button>
                  </div>
                  <pre className="text-xs font-mono text-cyan-300 bg-slate-950 p-3 rounded overflow-x-auto">
{`./push_to_github.sh ${githubUrlInput || 'https://github.com/YOUR_USERNAME/YOUR_REPO.git'}`}
                  </pre>
                </div>
              </div>
            </div>

            {/* Free Hosting Platforms */}
            <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 space-y-4">
              <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
                <div className="w-10 h-10 rounded-lg bg-slate-900 border border-slate-700 flex items-center justify-center text-teal-400">
                  <Globe className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white">2. Free Cloud Hosting Deployment Platforms</h3>
                  <p className="text-xs text-slate-400">Pre-configured configuration files are included for 1-click zero-cost deployments.</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* GitHub Pages */}
                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-white flex items-center gap-1.5">
                      <Github className="w-4 h-4 text-slate-300" />
                      <span>GitHub Pages</span>
                    </span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400">
                      Automated CI/CD
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Automated workflow file <code>.github/workflows/deploy.yml</code> is ready in the repository. On every <code>git push</code> to <code>main</code>, GitHub Actions builds and publishes your live site.
                  </p>
                  <div className="text-[11px] text-slate-500 pt-1">
                    <strong>Enable:</strong> In your GitHub repository, go to <em>Settings → Pages → Build and deployment → Source: GitHub Actions</em>.
                  </div>
                </div>

                {/* Vercel */}
                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-white flex items-center gap-1.5">
                      <UploadCloud className="w-4 h-4 text-blue-400" />
                      <span>Vercel</span>
                    </span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-blue-500/20 text-blue-400">
                      1-Click Free
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Pre-configured <code>vercel.json</code> included. Import your GitHub repository directly to Vercel for free global edge hosting with instant SSL and automatic preview URLs.
                  </p>
                  <a
                    href="https://vercel.com/new"
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 font-medium"
                  >
                    <span>Deploy on Vercel</span>
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </a>
                </div>

                {/* Netlify */}
                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-white flex items-center gap-1.5">
                      <Globe className="w-4 h-4 text-teal-400" />
                      <span>Netlify</span>
                    </span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-teal-500/20 text-teal-400">
                      1-Click Free
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Pre-configured <code>netlify.toml</code> included. Connect your GitHub repository on Netlify to build and deploy static web applications with continuous deployment.
                  </p>
                  <a
                    href="https://app.netlify.com/start"
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-xs text-teal-400 hover:text-teal-300 font-medium"
                  >
                    <span>Deploy on Netlify</span>
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </a>
                </div>

                {/* Render */}
                <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-white flex items-center gap-1.5">
                      <Terminal className="w-4 h-4 text-purple-400" />
                      <span>Render / Railway</span>
                    </span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-purple-500/20 text-purple-400">
                      Free Web & Python
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    Deploy native Python services, workers, or web servers with automated Git push triggers and free custom domain support.
                  </p>
                  <a
                    href="https://render.com"
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-xs text-purple-400 hover:text-purple-300 font-medium"
                  >
                    <span>Deploy on Render</span>
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            </div>

            {/* Cloud MySQL Integration with Deployed Apps */}
            <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 space-y-3">
              <h4 className="font-bold text-sm text-white flex items-center gap-2">
                <Database className="w-4 h-4 text-blue-400" />
                <span>Connecting Free Online Cloud MySQL on Your Hosting Platform</span>
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                When deploying on Vercel, Netlify, or Render, navigate to your project's <strong>Environment Variables</strong> settings and paste your 5 database credentials:
              </p>
              <div className="bg-slate-900 p-3.5 rounded-lg border border-slate-800 font-mono text-xs text-slate-300 space-y-1">
                <div>DB_HOST = your-free-cloud-host.aivencloud.com</div>
                <div>DB_PORT = 3306</div>
                <div>DB_NAME = defaultdb</div>
                <div>DB_USER = avnadmin</div>
                <div>DB_PASSWORD = your_password</div>
              </div>
              <p className="text-xs text-slate-400">
                To auto-provision tables and sample seed records on your free online cloud database, simply run <code>python init_database.py</code> locally in VS Code or in the cloud console. Zero workbench required!
              </p>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-slate-950 border-t border-slate-800 px-6 py-3 text-xs text-slate-500 flex flex-wrap items-center justify-between gap-2">
        <div>
          Student Record Management System &bull; Production Architecture &bull; Ready for Visual Studio Code
        </div>
        <div className="flex items-center gap-4">
          <a
            href="/student_record_management.zip"
            download="student_record_management.zip"
            className="text-emerald-400 hover:text-emerald-300 font-semibold"
          >
            Download ZIP Archive (79 KB)
          </a>
        </div>
      </footer>
    </div>
  );
}
