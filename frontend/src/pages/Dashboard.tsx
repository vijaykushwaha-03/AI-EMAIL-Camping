import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Mail, MousePointer, AlertTriangle, Plus, Sparkles } from 'lucide-react';
import { pageVariants, containerVariants } from '../lib/animations';
import { MetricCard } from '../components/dashboard/MetricCard';
import { PerformanceChart } from '../components/dashboard/PerformanceChart';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { getDashboardStats, type DashboardStats } from '../lib/api';
import styles from './Dashboard.module.css';

export function Dashboard() {
    const [data, setData] = useState<DashboardStats | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        getDashboardStats()
            .then(setData)
            .catch((e) => setError(e.message))
            .finally(() => setLoading(false));
    }, []);

    if (loading) {
        return (
            <div className={styles.loading}>
                <div className={styles.spinner}></div>
                <p>Loading dashboard...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className={styles.error}>
                <p>Error: {error}</p>
                <Button onClick={() => window.location.reload()}>Retry</Button>
            </div>
        );
    }

    const stats = data?.stats || { total_sent: 0, total_contacts: 0, open_rate: 0, click_rate: 0, bounce_rate: 0 };
    const chartData = data?.chart_data || [];
    const recentCampaigns = data?.recent_campaigns || [];

    return (
        <motion.div
            className={styles.dashboard}
            variants={pageVariants}
            initial="initial"
            animate="animate"
            exit="exit"
        >
            {/* Header */}
            <div className={styles.header}>
                <div>
                    <h1 className={styles.title}>Welcome back! 👋</h1>
                    <p className={styles.subtitle}>Here's what's happening with your campaigns</p>
                </div>
                <Button icon={<Plus size={18} />} onClick={() => window.location.href = '/campaigns/new'}>
                    New Campaign
                </Button>
            </div>

            {/* Metrics Grid */}
            <motion.div
                className={styles.metricsGrid}
                variants={containerVariants}
                initial="initial"
                animate="animate"
            >
                <MetricCard
                    title="Total Sent"
                    value={stats.total_sent}
                    icon={<Send size={20} />}
                    color="blue"
                />
                <MetricCard
                    title="Open Rate"
                    value={stats.open_rate}
                    suffix="%"
                    icon={<Mail size={20} />}
                    color="green"
                />
                <MetricCard
                    title="Click Rate"
                    value={stats.click_rate}
                    suffix="%"
                    icon={<MousePointer size={20} />}
                    color="purple"
                />
                <MetricCard
                    title="Bounce Rate"
                    value={stats.bounce_rate}
                    suffix="%"
                    icon={<AlertTriangle size={20} />}
                    color="orange"
                />
            </motion.div>

            {/* Charts and Recent Campaigns */}
            <motion.div
                className={styles.contentGrid}
                variants={containerVariants}
                initial="initial"
                animate="animate"
            >
                {/* Performance Chart */}
                <div className={styles.chartSection}>
                    <PerformanceChart data={chartData} />
                </div>

                {/* Recent Campaigns */}
                <Card className={styles.campaignsCard}>
                    <CardHeader>
                        <CardTitle>Recent Campaigns</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {recentCampaigns.length === 0 ? (
                            <p className={styles.empty}>No campaigns yet. Create your first one!</p>
                        ) : (
                            <div className={styles.campaignsList}>
                                {recentCampaigns.map((campaign) => (
                                    <motion.div
                                        key={campaign.id}
                                        className={styles.campaignItem}
                                        whileHover={{ x: 4 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                        <div className={styles.campaignInfo}>
                                            <span className={styles.campaignName}>{campaign.name}</span>
                                            <span className={styles.campaignDate}>
                                                {new Date(campaign.created_at).toLocaleDateString()}
                                            </span>
                                        </div>
                                        <div className={styles.campaignStats}>
                                            <span className={`${styles.status} ${styles[campaign.status]}`}>
                                                {campaign.status}
                                            </span>
                                            {campaign.open_rate > 0 && (
                                                <span className={styles.openRate}>{campaign.open_rate}%</span>
                                            )}
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Quick Actions */}
                <Card className={styles.actionsCard} gradient>
                    <CardContent>
                        <div className={styles.actionsContent}>
                            <Sparkles size={32} className={styles.actionsIcon} />
                            <h3>Create with AI</h3>
                            <p>Generate compelling email content in seconds</p>
                            <Button variant="secondary" icon={<Sparkles size={16} />} onClick={() => window.location.href = '/campaigns/new'}>
                                Try AI Generator
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </motion.div>
        </motion.div>
    );
}
