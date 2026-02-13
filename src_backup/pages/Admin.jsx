import React from 'react';
import { Package, User, MapPin, Truck, Check } from 'lucide-react';

export default function Admin() {
    const orders = [
        { id: '1001', customer: 'Ama Serwaa', plan: 'Daily Core', status: 'Pending', pressed: '4:30 AM', rider: 'Unassigned' },
        { id: '1002', customer: 'Kojo Mensah', plan: 'Office Pack', status: 'Delivered', pressed: '4:15 AM', rider: 'Kwame A.' },
        { id: '1003', customer: 'Sarah Doe', plan: 'Immunity Boost', status: 'In Transit', pressed: '4:45 AM', rider: 'Kwame A.' },
    ];

    return (
        <div className="container" style={{ paddingTop: '6rem', paddingBottom: '4rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Admin Dashboard</h1>
                <button className="btn btn-primary">Export Production List</button>
            </div>

            <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '3rem' }}>
                <div className="card">
                    <h3>Total Orders</h3>
                    <p style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--primary)' }}>24</p>
                    <p>Today</p>
                </div>
                <div className="card">
                    <h3>Active Riders</h3>
                    <p style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--accent)' }}>3</p>
                    <p>Online</p>
                </div>
                <div className="card">
                    <h3>Production</h3>
                    <p style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--text-main)' }}>98%</p>
                    <p>Completed</p>
                </div>
            </div>

            <div className="card">
                <h2 style={{ marginBottom: '1.5rem' }}>Recent Orders</h2>
                <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', minWidth: '600px' }}>
                        <thead>
                            <tr style={{ background: 'var(--bg-secondary)', textAlign: 'left' }}>
                                <th style={{ padding: '1rem' }}>Order ID</th>
                                <th style={{ padding: '1rem' }}>Customer</th>
                                <th style={{ padding: '1rem' }}>Plan</th>
                                <th style={{ padding: '1rem' }}>Pressed At</th>
                                <th style={{ padding: '1rem' }}>Status</th>
                                <th style={{ padding: '1rem' }}>Rider</th>
                                <th style={{ padding: '1rem' }}>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {orders.map(order => (
                                <tr key={order.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                                    <td style={{ padding: '1rem', fontWeight: '500' }}>#{order.id}</td>
                                    <td style={{ padding: '1rem' }}>{order.customer}</td>
                                    <td style={{ padding: '1rem' }}>
                                        <span style={{
                                            background: order.plan === 'Daily Core' ? '#dcfce7' : order.plan === 'Office Pack' ? '#e0e7ff' : '#fef3c7',
                                            color: order.plan === 'Daily Core' ? '#166534' : order.plan === 'Office Pack' ? '#3730a3' : '#92400e',
                                            padding: '0.25rem 0.5rem', borderRadius: '0.25rem', fontSize: '0.85rem', fontWeight: '600'
                                        }}>
                                            {order.plan}
                                        </span>
                                    </td>
                                    <td style={{ padding: '1rem', color: 'var(--text-muted)' }}>{order.pressed}</td>
                                    <td style={{ padding: '1rem' }}>
                                        <span style={{
                                            display: 'inline-flex', alignItems: 'center', gap: '0.5rem',
                                            color: order.status === 'Delivered' ? 'var(--primary)' : order.status === 'In Transit' ? 'var(--accent)' : 'var(--text-muted)',
                                            fontWeight: '500'
                                        }}>
                                            {order.status === 'Delivered' && <Check size={16} />}
                                            {order.status === 'In Transit' && <Truck size={16} />}
                                            {order.status === 'Pending' && <Package size={16} />}
                                            {order.status}
                                        </span>
                                    </td>
                                    <td style={{ padding: '1rem' }}>{order.rider}</td>
                                    <td style={{ padding: '1rem' }}>
                                        <button style={{ border: 'none', background: 'transparent', color: 'var(--primary)', cursor: 'pointer', fontWeight: 'bold' }}>Manage</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
