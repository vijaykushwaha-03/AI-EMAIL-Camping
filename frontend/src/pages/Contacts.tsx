import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, Upload, Search, Trash2, Mail } from 'lucide-react';
import { pageVariants, containerVariants, itemVariants } from '../lib/animations';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { getContacts, deleteContact, importContacts, type Contact, type ContactsResponse } from '../lib/api';
import styles from './Contacts.module.css';

export function Contacts() {
    const [contacts, setContacts] = useState<Contact[]>([]);
    const [total, setTotal] = useState(0);
    const [page, setPage] = useState(1);
    const [search, setSearch] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [importing, setImporting] = useState(false);

    useEffect(() => {
        loadContacts();
    }, [page, search]);

    const loadContacts = () => {
        setLoading(true);
        getContacts(page, search)
            .then((data: ContactsResponse) => {
                setContacts(data.results);
                setTotal(data.count);
            })
            .catch((e) => setError(e.message))
            .finally(() => setLoading(false));
    };

    const handleDelete = async (id: string) => {
        if (!confirm('Delete this contact?')) return;
        try {
            await deleteContact(id);
            setContacts(contacts.filter(c => c.id !== id));
            setTotal(total - 1);
        } catch {
            alert('Failed to delete');
        }
    };

    const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        setImporting(true);
        try {
            const result = await importContacts(file);
            alert(`Imported ${result.imported} contacts (${result.skipped} skipped)`);
            loadContacts();
        } catch {
            alert('Import failed');
        } finally {
            setImporting(false);
            e.target.value = '';
        }
    };

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        setPage(1);
        loadContacts();
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
                    <h1 className={styles.title}>Contacts</h1>
                    <p className={styles.subtitle}>{total} contacts in your list</p>
                </div>
                <div className={styles.actions}>
                    <label className={styles.importBtn}>
                        <input type="file" accept=".csv" onChange={handleImport} hidden />
                        <Button variant="secondary" icon={<Upload size={18} />} loading={importing}>
                            Import CSV
                        </Button>
                    </label>
                    <Button icon={<Plus size={18} />}>
                        Add Contact
                    </Button>
                </div>
            </div>

            {/* Search */}
            <form onSubmit={handleSearch} className={styles.searchBar}>
                <Search size={20} className={styles.searchIcon} />
                <input
                    type="text"
                    placeholder="Search contacts..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className={styles.searchInput}
                />
            </form>

            {/* Table */}
            <Card className={styles.tableCard}>
                {loading ? (
                    <div className={styles.loading}>Loading...</div>
                ) : error ? (
                    <div className={styles.error}>{error}</div>
                ) : contacts.length === 0 ? (
                    <div className={styles.empty}>
                        <Mail size={48} className={styles.emptyIcon} />
                        <h3>No contacts found</h3>
                        <p>Import a CSV or add contacts manually</p>
                    </div>
                ) : (
                    <motion.table
                        className={styles.table}
                        variants={containerVariants}
                        initial="initial"
                        animate="animate"
                    >
                        <thead>
                            <tr>
                                <th>Email</th>
                                <th>Name</th>
                                <th>Company</th>
                                <th>Status</th>
                                <th>Added</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {contacts.map((contact) => (
                                <motion.tr key={contact.id} variants={itemVariants}>
                                    <td className={styles.email}>{contact.email}</td>
                                    <td>{contact.name || '-'}</td>
                                    <td>{contact.company || '-'}</td>
                                    <td>
                                        <span className={`${styles.badge} ${contact.is_subscribed ? styles.active : styles.inactive}`}>
                                            {contact.is_subscribed ? 'Subscribed' : 'Unsubscribed'}
                                        </span>
                                    </td>
                                    <td className={styles.date}>
                                        {new Date(contact.created_at).toLocaleDateString()}
                                    </td>
                                    <td>
                                        <button className={styles.deleteBtn} onClick={() => handleDelete(contact.id)}>
                                            <Trash2 size={16} />
                                        </button>
                                    </td>
                                </motion.tr>
                            ))}
                        </tbody>
                    </motion.table>
                )}

                {/* Pagination */}
                {total > 25 && (
                    <div className={styles.pagination}>
                        <Button
                            variant="ghost"
                            size="sm"
                            disabled={page === 1}
                            onClick={() => setPage(page - 1)}
                        >
                            Previous
                        </Button>
                        <span>Page {page} of {Math.ceil(total / 25)}</span>
                        <Button
                            variant="ghost"
                            size="sm"
                            disabled={page * 25 >= total}
                            onClick={() => setPage(page + 1)}
                        >
                            Next
                        </Button>
                    </div>
                )}
            </Card>
        </motion.div>
    );
}
