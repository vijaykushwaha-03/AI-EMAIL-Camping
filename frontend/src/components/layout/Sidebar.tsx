import { NavLink, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    LayoutDashboard,
    Send,
    Users,
    FileText,
    BarChart3,
    Settings,
    Sparkles,
    Mail
} from 'lucide-react';
import { sidebarVariants } from '../../lib/animations';
import styles from './Sidebar.module.css';

const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/campaigns', icon: Send, label: 'Campaigns' },
    { path: '/contacts', icon: Users, label: 'Contacts' },
    { path: '/templates', icon: FileText, label: 'Templates' },
    { path: '/analytics', icon: BarChart3, label: 'Analytics' },
    { path: '/settings', icon: Settings, label: 'Settings' },
];

export function Sidebar() {
    const location = useLocation();

    return (
        <motion.aside
            className={styles.sidebar}
            variants={sidebarVariants}
            initial="initial"
            animate="animate"
        >
            {/* Logo */}
            <div className={styles.logo}>
                <div className={styles.logoIcon}>
                    <Mail size={24} />
                </div>
                <span className={styles.logoText}>
                    MailFlow <Sparkles size={14} className={styles.sparkle} />
                </span>
            </div>

            {/* Navigation */}
            <nav className={styles.nav}>
                {navItems.map((item) => {
                    const isActive = location.pathname === item.path;
                    const Icon = item.icon;

                    return (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            className={`${styles.navItem} ${isActive ? styles.active : ''}`}
                        >
                            <motion.div
                                className={styles.navContent}
                                whileHover={{ x: 4 }}
                                transition={{ duration: 0.2 }}
                            >
                                <Icon size={20} />
                                <span>{item.label}</span>
                            </motion.div>
                            {isActive && (
                                <motion.div
                                    className={styles.activeIndicator}
                                    layoutId="activeIndicator"
                                    transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                                />
                            )}
                        </NavLink>
                    );
                })}
            </nav>

            {/* Plan Status */}
            <div className={styles.planCard}>
                <div className={styles.planHeader}>
                    <Sparkles size={16} className={styles.planIcon} />
                    <span className={styles.planName}>Pro Plan</span>
                </div>
                <div className={styles.planUsage}>
                    <div className={styles.planProgress}>
                        <div
                            className={styles.planProgressBar}
                            style={{ width: '75%' }}
                        />
                    </div>
                    <span className={styles.planText}>7,500 / 10,000 emails</span>
                </div>
            </div>
        </motion.aside>
    );
}
