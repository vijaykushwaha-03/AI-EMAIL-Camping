import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, Send, Edit, Trash2, Search } from 'lucide-react';
import { pageVariants, containerVariants, itemVariants } from '../lib/animations';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { getCampaigns, deleteCampaign, type Campaign } from '../lib/api';
import styles from './Campaigns.module.css';

export function Campaigns() {
    const [campaigns, setCampaigns] = useState<Campaign[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadCampaigns();
    }, []);

    const loadCampaigns = () => {
        setLoading(true);
        getCampaigns()
            .then(setCampaigns)
            .catch((e) => setError(e.message))
            .finally(() => setLoading(false));
    };

    const handleDelete = async (id: string) => {
        if (!confirm('Are you sure you want to delete this campaign?')) return;
        try {
            await deleteCampaign(id);
            setCampaigns(campaigns.filter(c => c.id !== id));
        } catch (e: unknown) {
            alert('Failed to delete campaign');
        }
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'sent': return styles.statusSent;
            case 'draft': return styles.statusDraft;
            case 'scheduled': return styles.statusScheduled;
            case 'sending': return styles.statusSending;
            default: return '';
        }
    };

    return (
        <motion.div
            className={styles.page}
            variants={pageVariants}
            initial="initial"
            animate="animate"
        >
            <div className={styles.header}>
                <div>
                    <h1 className={styles.title}>Campaigns</h1>
                    <p className={styles.subtitle}>Manage your email campaigns</p>
                </div>
                <Button icon={<Plus size={18} />} onClick={() => window.location.href = '/campaigns/new'}>
                    New Campaign
                </Button>
            </div>

            {loading ? (
                <div className={styles.loading}>Loading campaigns...</div>
            ) : error ? (
                <div className={styles.error}>{error}</div>
            ) : campaigns.length === 0 ? (
                <Card className={styles.empty}>
                    <div className={styles.emptyContent}>
                        <Send size={48} className={styles.emptyIcon} />
                        <h3>No campaigns yet</h3>
                        <p>Create your first email campaign to start reaching your audience.</p>
                        <Button icon={<Plus size={18} />} onClick={() => window.location.href = '/campaigns/new'}>
                            Create Campaign
                        </Button>
                    </div>
                </Card>
            ) : (
                <motion.div
                    className={styles.grid}
                    variants={containerVariants}
                    initial="initial"
                    animate="animate"
                >
                    {campaigns.map((campaign) => (
                        <motion.div key={campaign.id} variants={itemVariants}>
                            <Card hover className={styles.campaignCard}>
                                <div className={styles.cardHeader}>
                                    <h3 className={styles.campaignName}>{campaign.name}</h3>
                                    <span className={`${styles.status} ${getStatusColor(campaign.status)}`}>
                                        {campaign.status}
                                    </span>
                                </div>
                                <p className={styles.subject}>{campaign.subject}</p>
                                <div className={styles.stats}>
                                    <div className={styles.stat}>
                                        <span className={styles.statValue}>{campaign.sent_count}</span>
                                        <span className={styles.statLabel}>Sent</span>
                                    </div>
                                    <div className={styles.stat}>
                                        <span className={styles.statValue}>{campaign.open_rate}%</span>
                                        <span className={styles.statLabel}>Opened</span>
                                    </div>
                                    <div className={styles.stat}>
                                        <span className={styles.statValue}>{campaign.click_rate}%</span>
                                        <span className={styles.statLabel}>Clicked</span>
                                    </div>
                                </div>
                                <div className={styles.cardFooter}>
                                    <span className={styles.date}>
                                        {new Date(campaign.created_at).toLocaleDateString()}
                                    </span>
                                    <div className={styles.actions}>
                                        <button className={styles.iconBtn} onClick={() => window.location.href = `/campaigns/${campaign.id}`}>
                                            <Edit size={16} />
                                        </button>
                                        <button className={styles.iconBtn} onClick={() => handleDelete(campaign.id)}>
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                </div>
                            </Card>
                        </motion.div>
                    ))}
                </motion.div>
            )}
        </motion.div>
    );
}
