import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, ArrowRight, Sparkles, Send, Eye } from 'lucide-react';
import { useParams, useNavigate } from 'react-router-dom';
import { pageVariants } from '../lib/animations';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { createCampaign, generateEmail, sendCampaign, getCampaign, updateCampaign } from '../lib/api';
import styles from './CampaignNew.module.css';

type Step = 'details' | 'content' | 'preview' | 'send';

export function CampaignNew() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [step, setStep] = useState<Step>('details');
    const [loading, setLoading] = useState(false);
    const [generating, setGenerating] = useState(false);
    const [fetching, setFetching] = useState(false);

    const [form, setForm] = useState({
        name: '',
        subject: '',
        content: '',
        cc_email: '',
        bcc_email: '',
        prompt: ''
    });

    const [campaignId, setCampaignId] = useState<string | null>(null);
    const [sendResult, setSendResult] = useState<{ sent: number; failed: number } | null>(null);

    useEffect(() => {
        if (id) {
            setCampaignId(id);
            loadCampaign(id);
        }
    }, [id]);

    const loadCampaign = async (id: string) => {
        setFetching(true);
        try {
            const campaign = await getCampaign(id);
            setForm({
                name: campaign.name,
                subject: campaign.subject,
                content: campaign.content,
                cc_email: campaign.cc_email || '',
                bcc_email: campaign.bcc_email || '',
                prompt: ''
            });
        } catch (e) {
            alert('Failed to load campaign');
            navigate('/campaigns');
        } finally {
            setFetching(false);
        }
    };

    const handleGenerate = async () => {
        if (!form.prompt) {
            alert('Please enter a prompt first');
            return;
        }
        setGenerating(true);
        try {
            const result = await generateEmail(form.prompt);
            setForm({
                ...form,
                subject: result.subject,
                content: `<h2>${result.title}</h2><p>${result.body}</p><button style="background:#3b82f6;color:white;padding:12px 24px;border:none;border-radius:8px;cursor:pointer;">${result.cta_text}</button>`
            });
        } catch (e: unknown) {
            const errorMsg = e instanceof Error ? e.message : 'Unknown error';
            alert(`Failed to generate: ${errorMsg}`);
            console.error('Generate error:', e);
        } finally {
            setGenerating(false);
        }
    };

    const handleSave = async () => {
        setLoading(true);
        try {
            if (campaignId) {
                await updateCampaign(campaignId, {
                    name: form.name,
                    subject: form.subject,
                    content: form.content,
                    cc_email: form.cc_email,
                    bcc_email: form.bcc_email
                });
            } else {
                const campaign = await createCampaign({
                    name: form.name,
                    subject: form.subject,
                    content: form.content,
                    cc_email: form.cc_email,
                    bcc_email: form.bcc_email
                });
                setCampaignId(campaign.id);
            }
            setStep('preview');
        } catch (e: unknown) {
            alert('Failed to save campaign');
        } finally {
            setLoading(false);
        }
    };

    const handleSend = async (testMode = false) => {
        if (!campaignId) return;
        setLoading(true);
        try {
            const result = await sendCampaign(campaignId, testMode);
            setSendResult({ sent: result.sent, failed: result.failed });
            setStep('send');
        } catch (e: unknown) {
            alert('Failed to send campaign');
        } finally {
            setLoading(false);
        }
    };

    const steps: Step[] = ['details', 'content', 'preview', 'send'];
    const currentIndex = steps.indexOf(step);

    if (fetching) {
        return <div className={styles.loading}>Loading campaign...</div>;
    }

    return (
        <motion.div
            className={styles.page}
            variants={pageVariants}
            initial="initial"
            animate="animate"
        >
            <div className={styles.header}>
                <button className={styles.backBtn} onClick={() => navigate('/campaigns')}>
                    <ArrowLeft size={20} /> Back to Campaigns
                </button>
                <h1>{id ? 'Edit Campaign' : 'Create New Campaign'}</h1>
            </div>

            {/* Progress */}
            <div className={styles.progress}>
                {steps.map((s, i) => (
                    <div key={s} className={`${styles.step} ${i <= currentIndex ? styles.active : ''}`}>
                        <div className={styles.stepNumber}>{i + 1}</div>
                        <span className={styles.stepLabel}>{s.charAt(0).toUpperCase() + s.slice(1)}</span>
                    </div>
                ))}
            </div>

            <Card className={styles.formCard}>
                {/* Step: Details */}
                {step === 'details' && (
                    <div className={styles.stepContent}>
                        <h2>Campaign Details</h2>
                        <div className={styles.field}>
                            <label>Campaign Name</label>
                            <input
                                type="text"
                                value={form.name}
                                onChange={(e) => setForm({ ...form, name: e.target.value })}
                                placeholder="e.g., Summer Sale Announcement"
                            />
                        </div>
                        <div className={styles.row}>
                            <div className={styles.field}>
                                <label>CC Email (Optional)</label>
                                <input
                                    type="email"
                                    value={form.cc_email}
                                    onChange={(e) => setForm({ ...form, cc_email: e.target.value })}
                                    placeholder="manager@example.com"
                                />
                                <small className={styles.hint}>Receives a copy of EVERY email sent.</small>
                            </div>
                            <div className={styles.field}>
                                <label>BCC Email (Optional)</label>
                                <input
                                    type="email"
                                    value={form.bcc_email}
                                    onChange={(e) => setForm({ ...form, bcc_email: e.target.value })}
                                    placeholder="archive@example.com"
                                />
                                <small className={styles.hint}>Hidden copy of EVERY email sent.</small>
                            </div>
                        </div>
                        <div className={styles.actions}>
                            <Button
                                onClick={() => setStep('content')}
                                disabled={!form.name}
                                icon={<ArrowRight size={18} />}
                                iconPosition="right"
                            >
                                Next: Content
                            </Button>
                        </div>
                    </div>
                )}

                {/* Step: Content */}
                {step === 'content' && (
                    <div className={styles.stepContent}>
                        <h2>Email Content</h2>

                        {/* AI Generator */}
                        <div className={styles.aiBox}>
                            <Sparkles size={20} className={styles.aiIcon} />
                            <div className={styles.aiContent}>
                                <h3>Generate with AI</h3>
                                <input
                                    type="text"
                                    value={form.prompt}
                                    onChange={(e) => setForm({ ...form, prompt: e.target.value })}
                                    placeholder="Describe your email... e.g., 'Announce 50% off summer sale'"
                                />
                                <Button
                                    variant="secondary"
                                    size="sm"
                                    onClick={handleGenerate}
                                    loading={generating}
                                    icon={<Sparkles size={16} />}
                                >
                                    Generate
                                </Button>
                            </div>
                        </div>

                        <div className={styles.field}>
                            <label>Subject Line</label>
                            <input
                                type="text"
                                value={form.subject}
                                onChange={(e) => setForm({ ...form, subject: e.target.value })}
                                placeholder="Email subject"
                            />
                        </div>

                        <div className={styles.field}>
                            <label>Content (HTML)</label>
                            <textarea
                                value={form.content}
                                onChange={(e) => setForm({ ...form, content: e.target.value })}
                                placeholder="<h2>Your Title</h2><p>Your content...</p>"
                                rows={10}
                            />
                        </div>

                        <div className={styles.actions}>
                            <Button variant="ghost" onClick={() => setStep('details')}>
                                <ArrowLeft size={18} /> Back
                            </Button>
                            <Button
                                onClick={handleSave}
                                disabled={!form.subject || !form.content}
                                loading={loading}
                                icon={<Eye size={18} />}
                            >
                                {id ? 'Update & Preview' : 'Create & Preview'}
                            </Button>
                        </div>
                    </div>
                )}

                {/* Step: Preview */}
                {step === 'preview' && (
                    <div className={styles.stepContent}>
                        <h2>Preview Campaign</h2>
                        <div className={styles.preview}>
                            <div className={styles.previewHeader}>
                                <strong>Subject:</strong> {form.subject}
                            </div>
                            {(form.cc_email || form.bcc_email) && (
                                <div className={styles.previewMeta}>
                                    {form.cc_email && <div><strong>CC:</strong> {form.cc_email}</div>}
                                    {form.bcc_email && <div><strong>BCC:</strong> {form.bcc_email}</div>}
                                </div>
                            )}
                            <div
                                className={styles.previewBody}
                                dangerouslySetInnerHTML={{ __html: form.content }}
                            />
                        </div>
                        <div className={styles.actions}>
                            <Button variant="ghost" onClick={() => setStep('content')}>
                                <ArrowLeft size={18} /> Edit
                            </Button>
                            <Button variant="secondary" onClick={() => handleSend(true)} loading={loading}>
                                Send Test
                            </Button>
                            <Button onClick={() => handleSend(false)} loading={loading} icon={<Send size={18} />}>
                                Send Campaign
                            </Button>
                        </div>
                    </div>
                )}

                {/* Step: Send Complete */}
                {step === 'send' && sendResult && (
                    <div className={styles.stepContent}>
                        <div className={styles.success}>
                            <Send size={48} className={styles.successIcon} />
                            <h2>Campaign Sent!</h2>
                            <p>Successfully sent to <strong>{sendResult.sent}</strong> recipients</p>
                            {sendResult.failed > 0 && (
                                <p className={styles.failed}>{sendResult.failed} failed</p>
                            )}
                            <Button onClick={() => navigate('/campaigns')}>
                                Back to Campaigns
                            </Button>
                        </div>
                    </div>
                )}
            </Card>
        </motion.div>
    );
}
