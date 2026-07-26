"""add_hnsw_index_and_rls

Revision ID: dcf500ad827d
Revises: a9f935f8b1ab
Create Date: 2026-07-26 08:47:03.858074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dcf500ad827d'
down_revision: Union[str, None] = 'a9f935f8b1ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # HNSW vector index for semantic search
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_document_chunks_embedding_hnsw "
        "ON document_chunks "
        "USING hnsw (embedding vector_cosine_ops)"
    )

    # RLS: enable row-level security on user-scoped tables
    op.execute("ALTER TABLE profiles ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE chat_threads ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE message_citations ENABLE ROW LEVEL SECURITY")

    # Public corpus tables: authenticated users can read
    op.execute("ALTER TABLE source_documents ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY")

    # Profiles: users can read/update their own
    op.execute(
        "CREATE POLICY profiles_user_isolation ON profiles "
        "USING (id = auth.uid()) "
        "WITH CHECK (id = auth.uid())"
    )

    # Chat threads: users see only their own
    op.execute(
        "CREATE POLICY chat_threads_user_isolation ON chat_threads "
        "USING (user_id = auth.uid()) "
        "WITH CHECK (user_id = auth.uid())"
    )

    # Chat messages: through thread ownership
    op.execute(
        "CREATE POLICY chat_messages_user_isolation ON chat_messages "
        "USING (thread_id IN (SELECT id FROM chat_threads WHERE user_id = auth.uid())) "
        "WITH CHECK (thread_id IN (SELECT id FROM chat_threads WHERE user_id = auth.uid()))"
    )

    # Message citations: through message → thread ownership
    op.execute(
        "CREATE POLICY message_citations_user_isolation ON message_citations "
        "USING (message_id IN (SELECT id FROM chat_messages WHERE thread_id IN "
        "(SELECT id FROM chat_threads WHERE user_id = auth.uid()))) "
        "WITH CHECK (message_id IN (SELECT id FROM chat_messages WHERE thread_id IN "
        "(SELECT id FROM chat_threads WHERE user_id = auth.uid())))"
    )

    # Source documents: all authenticated users can read
    op.execute(
        "CREATE POLICY source_documents_read_all ON source_documents "
        "FOR SELECT USING (auth.role() = 'authenticated')"
    )

    # Document chunks: all authenticated users can read
    op.execute(
        "CREATE POLICY document_chunks_read_all ON document_chunks "
        "FOR SELECT USING (auth.role() = 'authenticated')"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_document_chunks_embedding_hnsw")

    op.execute("DROP POLICY IF EXISTS profiles_user_isolation ON profiles")
    op.execute("DROP POLICY IF EXISTS chat_threads_user_isolation ON chat_threads")
    op.execute("DROP POLICY IF EXISTS chat_messages_user_isolation ON chat_messages")
    op.execute("DROP POLICY IF EXISTS message_citations_user_isolation ON message_citations")
    op.execute("DROP POLICY IF EXISTS source_documents_read_all ON source_documents")
    op.execute("DROP POLICY IF EXISTS document_chunks_read_all ON document_chunks")

    op.execute("ALTER TABLE profiles DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE chat_threads DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE chat_messages DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE message_citations DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE source_documents DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE document_chunks DISABLE ROW LEVEL SECURITY")
